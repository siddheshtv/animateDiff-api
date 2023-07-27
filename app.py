import os
import yaml
import subprocess
import uuid
from flask import Flask, Response, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/prompt/', methods=['POST'])
def handle_prompt():
    global sample_data
    data = request.json
    promptData = data.get('prompt', '')
    prompt = promptData
    
    response = {'message': 'Prompt received successfully.'}

    sample_data = {
    "ToonYou": {
        "base": "",
        "path": "models/DreamBooth_LoRA/toonyou_beta3.safetensors",
        "motion_module": [
        "models/Motion_Module/mm_sd_v14.ckpt",
        "models/Motion_Module/mm_sd_v15.ckpt"
        ],
        "seed": [
        10788741199826055526,
        6520604954829636163,
        6519455744612555650,
        16372571278361863751
        ],
        "steps": 25,
        "guidance_scale": 7.5,
        "prompt": [
        prompt
        ],
        "n_prompt": [
        "",
        "badhandv4,easynegative,ng_deepnegative_v1_75t,verybadimagenegative_v1.3, bad-artist, bad_prompt_version2-neg, teeth",
        "",
        ""
        ]
    }
    }

    custom_yaml(sample_data)
    print("Prompt received successfully")
    return jsonify(response)

path_to_your_folder = "C:/Users/siddh/Downloads"


def custom_yaml(sample_data):
    yaml_content = yaml.dump(sample_data, default_flow_style=False)
    
    random_name = str(uuid.uuid4())[:8]  
    yaml_file_name = f"{random_name}.yaml"
    
    yaml_file_path = os.path.join(path_to_your_folder, yaml_file_name)
    with open(yaml_file_path, 'w') as yaml_file:
        yaml_file.write(yaml_content)
    
    response = Response(yaml_content, content_type='text/yaml')
    response.headers['Content-Disposition'] = f'attachment; filename={yaml_file_name}'
    
    execute_command(yaml_file_path)
    
    return response

def execute_command(yaml_file_path):
    command = f'python -m scripts.animate --config {yaml_file_path} --pretrained_model_path /content/animatediff/models/StableDiffusion --L 16 --W 512 --H 512'
    
    try:
        subprocess.run(command, shell=True, check=True)
        print("command ran successfully")
    except subprocess.CalledProcessError as e:
        print(f"Command execution failed: {e}")

if __name__ == '__main__':
    app.run(debug=True)
