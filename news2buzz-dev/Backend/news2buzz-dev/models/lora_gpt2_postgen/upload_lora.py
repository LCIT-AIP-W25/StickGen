from huggingface_hub import HfApi, upload_folder

# Initialize the API client
api = HfApi()

# Your model repo ID (username/repo-name)
repo_id = "anjithamohan/lora-gpt2-postgen"

# ✅ Create the model repository
api.create_repo(repo_id=repo_id, repo_type="model", exist_ok=True)

# ✅ Upload the local lora-output folder to the repo
upload_folder(
    folder_path="lora-output",   # Your local folder name
    path_in_repo="",             # Upload at root of the repo
    repo_id=repo_id,             # Full repo ID
    repo_type="model"
)
