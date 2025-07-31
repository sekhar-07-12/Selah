import streamlit as st
from modules import notes_manager, speech_to_text, qa_from_notes, journal_ai, drive_sync
from ui import theming
from utils import file_io
import os

# Set up page config and theming
st.set_page_config(page_title="Selah - AI Educational Assistant", layout="wide")
theming.set_theme()

# Sidebar navigation menu
st.sidebar.title("Selah 📚")
menu_options = [
    "Notes Manager 📄",
    "Speech to Text 🎙️",
    "Q&A from Notes ❓",
    "Reflective Journal 📔",
    "Google Drive Sync ☁️ (Optional)",
]

choice = st.sidebar.radio("Select Module", menu_options)

# Create data folder and files if not exist
os.makedirs("data", exist_ok=True)
for file_name in ["notes_data.json", "user_stats.json", "quizzes.json"]:
    file_path = os.path.join("data", file_name)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            if file_name == "user_stats.json":
                f.write("[]")  # Journal entries as list
            else:
                f.write("[]")  # Empty list for notes/quizzes

### Module 1: Notes Manager ###
if choice == "Notes Manager 📄":
    st.header("📄 Notes Manager")
    
    notes = notes_manager.load_notes()
    
    # Display notes titles for selection
    titles = [note["title"] for note in notes]
    selected_note_index = st.selectbox("Select a note to view or edit", options=[-1]+list(range(len(titles))),
                                       format_func=lambda x: "New Note" if x == -1 else titles[x])
    
    if selected_note_index == -1:
        # New note UI
        new_title = st.text_input("Note Title")
        new_content = st.text_area("Note Content")
        if st.button("Add Note"):
            if new_title.strip() == "" or new_content.strip() == "":
                st.warning("Title and content cannot be empty.")
            else:
                notes_manager.add_note(new_title.strip(), new_content.strip())
                st.success("Note added.")
                st.experimental_rerun()
    else:
        # Existing note view/edit/delete
        note = notes[selected_note_index]
        title = st.text_input("Title", value=note["title"])
        content = st.text_area("Content", value=note["content"])

        if st.button("Update Note"):
            notes_manager.edit_note(selected_note_index, title=title.strip(), content=content.strip())
            st.success("Note updated.")
            st.experimental_rerun()

        if st.button("Delete Note"):
            notes_manager.delete_note(selected_note_index)
            st.success("Note deleted.")
            st.experimental_rerun()

### Module 2: Speech to Text ###
elif choice == "Speech to Text 🎙️":
    st.header("🎙️ Speech to Text (Offline Dictation)")
    st.write("Press the button and speak clearly for 5 seconds.")
    
    if st.button("Start Dictation"):
        # Vosk model path (assumed to be in project root folder)
        text = speech_to_text.offline_speech_to_text(duration=5)
        st.text_area("Transcribed Text:", value=text, height=150)

### Module 3: Q&A from Notes ###
elif choice == "Q&A from Notes ❓":
    st.header("❓ Ask Questions Based on Your Notes")
    notes = qa_from_notes.load_notes()
    question = st.text_input("Enter your question here:")
    if st.button("Get Answer"):
        if question.strip() == "":
            st.warning("Please enter a question.")
        else:
            answer = qa_from_notes.answer_query(question.strip(), notes)
            st.success("Answer:")
            st.write(answer)

### Module 4: Reflective Journal ###
elif choice == "Reflective Journal 📔":
    st.header("📔 Reflective Journal")
    journal_entry = st.text_area("Write your reflective journal entry:")
    if st.button("Save Entry"):
        if journal_entry.strip() == "":
            st.warning("Journal entry cannot be empty.")
        else:
            journal_ai.add_journal_entry(journal_entry.strip())
            feedback = journal_ai.get_mood_feedback(journal_entry.strip())
            st.success("Entry saved.")
            st.info(feedback)

    # Display previous entries
    st.subheader("Previous Entries")
    entries = journal_ai.load_journal()
    if not entries:
        st.write("No journal entries found.")
    else:
        for entry in reversed(entries[-5:]):  # show last 5 entries
            st.markdown(f"**{entry['date']}**: {entry['entry']}")

### Module 5: Google Drive Sync ###
elif choice == "Google Drive Sync ☁️ (Optional)":
    st.header("☁️ Google Drive Sync (Optional)")
    st.info(
        """
        Use this module to back up your data files to Google Drive or download backups.
        Requires internet and valid `credentials.json` in the project root.
        """
    )

    uploaded_file = st.file_uploader("Upload a file to Drive (choose your local JSON backup):")
    if uploaded_file:
        # Save uploaded file locally before upload
        save_path = os.path.join("data", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File saved locally as {uploaded_file.name}")

        if st.button("Upload to Google Drive"):
            try:
                msg = drive_sync.upload_file(save_path)
                st.success(msg)
            except Exception as e:
                st.error(f"Upload failed: {e}")

    st.markdown("---")
    st.write("To download a file from Google Drive, enter the File ID below.")
    file_id = st.text_input("Google Drive File ID:")
    download_path = st.text_input("Save locally as (filename):", value="downloaded_backup.json")

    if st.button("Download from Google Drive"):
        try:
            msg = drive_sync.download_file(file_id.strip(), os.path.join("data", download_path.strip()))
            st.success(msg)
        except Exception as e:
            st.error(f"Download failed: {e}")

else:
    st.write("Select a module from the sidebar to get started.")
