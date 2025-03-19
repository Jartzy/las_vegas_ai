🚀 AI Collaboration Template Message for Checkpoints

Which AI: OpenAI ChatGPT
(Adjust this line if you’re using a different AI, e.g., “Bard by Google,” “Claude by Anthropic,” etc.)

📝 Checkpoint System Overview

I am using a file-based checkpoint system to track long-term projects. You must follow this format so that I can keep multiple AI assistants in sync.

🚀 What You Need to Do:
	1.	Every 50-100 messages, generate a checkpoint summarizing progress.
	2.	When starting a new chat, always ask:
	“Do you have a previous checkpoint file (e.g., checkpoint_2000_YYYY-MM-DD.json or .md)? If so, please upload it, and I’ll restore the context.”
	3.	If I upload a checkpoint file, process it and summarize key details.

📂 Checkpoint Format

Each checkpoint should be saved as JSON (.json) or Markdown (.md) with the following structure:

📌 File Naming Format:

checkpoint_[number]_[YYYY-MM-DD].json

Example:
	•	checkpoint_2000_2025-02-14.json
	•	checkpoint_1500_2025-01-20.md

📝 Example Checkpoint (Markdown Format)

📝 Checkpoint #2000 – AI Event Recommender Progress
📅 Date: February 14, 2025
🔢 Total Messages Since Last Checkpoint: 75

🧩 Recent Work Completed:
✅ Built content-based filtering using TF-IDF.
✅ Implemented collaborative filtering with SVD.
✅ Developed API structure for real-time recommendations.

⏳ Current Work in Progress:
- Testing API deployment with FastAPI.
- Evaluating cloud storage options (Google Drive vs AWS).

🔜 Next Steps:
1. Optimize API performance.
2. Implement real-time tracking for recommendations.
3. Choose cloud storage for long-term event storage.

📌 Notes:
If I need to reset this chat, please refer to this checkpoint to continue seamlessly.

🔄 Restoring Context in a New Chat
	1.	If I upload a previous checkpoint file, immediately process it and summarize key details.
	2.	If I don’t provide a checkpoint, ask:
	“Would you like to provide a previous checkpoint file to continue from the last known progress?”
	3.	If multiple checkpoint files exist, summarize the latest one unless I request more history.

📌 Question for the AI

“Would you like me to upload the latest checkpoint now?”

🚀 Template for Continuing a Project

If an AI already understands the system, you don’t need to send the full prompt—just provide the latest checkpoint.

Example:

	Here’s the latest checkpoint file for this project: checkpoint_2000_2025-02-14.json.
Please process it and summarize the last known progress before we continue.

🚀 How This Helps You
	•	Consistent AI responses across different sessions.
	•	No need to repeat long explanations—AI assistants just read the checkpoint file.
	•	Seamless context switching between AI instances without losing progress.
