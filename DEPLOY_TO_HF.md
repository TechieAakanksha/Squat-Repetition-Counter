# Deploy to Hugging Face Spaces - Step by Step

## Step 1: Get Your Hugging Face Token

1. Go to: https://huggingface.co/settings/tokens
2. Click "New token"
3. Name: "Git Access"
4. Permissions: **Write**
5. Click "Generate token"
6. **Copy the token** (you'll need it for the next step)

## Step 2: Authenticate Git with Token

Run this command (replace `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` with your actual token):

```bash
git remote set-url hf https://aakankshapatidar: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@huggingface.co/spaces/aakankshapatidar/Posturepal
```

## Step 3: Force Push Your Code to Hugging Face

Since the Space has different history, we'll force push your local code:

```bash
git push hf main --force
```

⚠️ **Note:** `--force` will overwrite whatever is in the HF Space with your local code. This is fine for initial deployment.

## Step 4: Check Your Space

Go to: https://huggingface.co/spaces/aakankshapatidar/Posturepal

The build will start automatically. It takes 2-5 minutes.

## Your Deployed URL:
`https://aakankshapatidar-posturepal.hf.space`

---

## Alternative: If You Prefer Not to Use Force Push

If you want to merge instead:

```bash
# Pull with unrelated histories allowed
git pull hf main --allow-unrelated-histories --no-edit

# Resolve any conflicts if needed, then:
git push hf main
```

But force push is simpler for initial deployment.

