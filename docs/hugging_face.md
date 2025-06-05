## Creating a Hugging Face Access Token

To use certain models and pipelines (such as WhisperX) that require authenticated access on Hugging Face, you’ll need to generate a personal access token.

Follow these steps:

---

### Step 1: Create a Hugging Face Account

If you don’t already have one, sign up here:  
[https://huggingface.co/join](https://huggingface.co/join)

---

### Step 2: Generate an Access Token

1. Go to your Hugging Face account's **Settings > Access Tokens**:  
   [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

2. Click **"Create new token"**.

3. Choose a **name** for the token.

4. Under **Role**, choose:  
   `Read` (recommended unless you plan to upload or manage models).

5. Click **"Generate"**.

6. Copy the token and store it securely.

   > ⚠️ Hugging Face will **not show it again**, so keep it safe (you can regenerate it if needed).

---

### Step 3: Add the Token to Your Project

- Add token to **HF_TOKEN** in file `scripts/config.py`

### Step 4: Accept User Agreement to 

For speaker diarization the following models require user agreement otherwise diarization will fail. Click on each link and follow direction for accepting user agreement.

- [pyannote/embedding](https://huggingface.co/pyannote/embedding)
- [pyannote/speaker-diarization](https://huggingface.co/pyannote/speaker-diarization)

---