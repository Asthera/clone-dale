from flask import Flask, render_template_string, request
from diffusers import DiffusionPipeline
import torch
from PIL import Image
import base64
from io import BytesIO

app = Flask(__name__)

# Initialize the model only once to save resource
pipe = DiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16)
pipe.to("cuda")


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the prompt from the form
        prompt = request.form.get('prompt')

        # Generate an image based on the prompt
        with torch.no_grad():  # Ensure to not track gradients
            images = pipe(prompt=prompt).images[0]

        # Convert the generated image to a format that can be displayed in HTML
        buffered = BytesIO()
        images.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # HTML content with the image embedded
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Simple App</title>
        </head>
        <body>
            <h1>Welcome to Our Simple Flask App</h1>
            <form action="/" method="post">
                <input type="text" name="prompt" placeholder="Enter a prompt">
                <input type="submit">
            </form>
            <h2>Prompt: {prompt}</h2>
            <img src="data:image/jpeg;base64,{img_str}" />
        </body>
        </html>
        """
    else:
        # Show the form for the GET request
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Simple App</title>
        </head>
        <body>
            <h1>Welcome to Our Simple Flask App</h1>
            <form action="/" method="post">
                <input type="text" name="prompt" placeholder="Enter a prompt">
                <input type="submit">
            </form>
        </body>
        </html>
        """


if __name__ == '__main__':
    app.run(debug=True)