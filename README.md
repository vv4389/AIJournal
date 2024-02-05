# JournalAI 📖

**Elevate Your Journaling Experience with AI!**
Welcome to JournalAI, where the magic of journaling meets the sophistication of artificial intelligence. 🚀 Users can effortlessly transform their photos into personalized, AI-crafted journal entries, making each memory a unique and enchanting narrative.
## ✨ Key Features

- **AI-Generated Journal Entries:** Utilize advanced AI to create personalized narratives from uploaded photos.
- **Seamless Integration:** Integrates with Google Location and Weather APIs for added context.
- **Secure Image Storage:** Store user-uploaded images securely on Google Storage with fine-grain access controls.
- **Manual Metadata Entry:** Provision for users to manually enter missing metadata through an intuitive interface.

## 🌐 System Flow:
**User Interaction:**
- Begin your journey by uploading photos through our streamlined and user-friendly interface.

**Metadata Handling:**
- Our system checks for essential metadata. If missing, you have the flexibility to manually input details through a user-friendly interface.
  
**Google Location API:**
- Let the Google Location API extract location metadata, enriching your narrative with a sense of place.

**VisualCrossing API (Weather Data):**
- Elevate your story with weather data from the VisualCrossing API, creating a rich and contextualized journal entry.

**Google Storage for Image Storage:**
- Entrust your memories to us. We securely store your images on Google Storage with fine-grain access controls.

**LLAVA-13B Model via Replicate API:**
- The heart of the magic lies in the LLAVA-13B model, seamlessly integrated through Replicate for AI-generated journal entries.

**Error Logging and Caching:**
- Our robust system logs errors and implements caching for optimal performance and reliability.

**User Output:**
- Witness the transformation! Your final AI-generated journal entry, complete with location, weather data, and personal touches.

## 🛠️ Tech Stack

- Python
- Streamlit for Frontend
- Google Cloud Services (Location API, Storage API)
- VisualCrossing API
- LLAVA-13B Model via Replicate API
- Error Logging and Caching Implementation for Robust Performance

## 🚀 Getting Started:
**Clone the Repository:**
git clone https://github.com/your-username/JournalAI.git

**Install Dependencies:**
pip install -r requirements.txt

**Run the Application:**
streamlit run app.py
