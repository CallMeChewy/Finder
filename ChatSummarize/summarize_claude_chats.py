import os
import re
from datetime import datetime

def summarize_claude_chats():
    """
    Summarizes Claude chat logs from a specified directory and creates a hyperlinked markdown file.
    """
    directory = "/home/herb/Desktop/Claude Conversations/"
    output_file = "Claude_Code_Chats_Summary.md"
    files = sorted([f for f in os.listdir(directory) if f.endswith('.md')])

    with open(output_file, 'w') as f:
        # --- Write Header ---
        start_match = re.search(r'claude-conversation-(\d{4}-\d{2}-\d{2})', files[0])
        end_match = re.search(r'claude-conversation-(\d{4}-\d{2}-\d{2})', files[-1])
        if start_match and end_match:
            start_date_str = start_match.group(1)
            end_date_str = end_match.group(1)
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').strftime('%m-%d-%Y')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').strftime('%m-%d-%Y')
            f.write(f"# Summary of Claude Chats for {start_date} thru {end_date}\n\n")
        else:
            f.write(f"# Summary of Claude Chats\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%m-%d-%Y %I:%M %p')}\n\n")

        # --- Write Index ---
        f.write("## Session Index\n\n")
        f.write("| Session | Date | Subject |\n")
        f.write("|---|---|---|\n")

        session_data = []
        for i, filename in enumerate(files):
            session_num = f"{i+1:04d}"
            match = re.search(r'claude-conversation-(\d{4}-\d{2}-\d{2})', filename)
            if match:
                date_str = match.group(1)
                dt_obj = datetime.strptime(date_str, '%Y-%m-%d')
                formatted_date = dt_obj.strftime('%m-%d-%Y - %A')
                
                with open(os.path.join(directory, filename), 'r') as chat_file:
                    content = chat_file.read()
                    # Simple subject extraction: first line of user prompt
                    user_prompt_match = re.search(r'\*\*User:\*\*\n(.*?)\n', content, re.DOTALL)
                    subject = "No subject found"
                    if user_prompt_match:
                        subject = user_prompt_match.group(1).strip().split('\n')[0]
                        subject = (subject[:70] + '...') if len(subject) > 70 else subject

                session_link = f"session-{session_num}"
                f.write(f"| {session_num} | {formatted_date} | [{subject}](#{session_link}) |\n")
                session_data.append({
                    "session_num": session_num,
                    "filename": filename,
                    "formatted_date": formatted_date,
                    "subject": subject,
                    "session_link": session_link,
                    "content": content
                })
        f.write("\n---\n\n")

        # --- Write Summaries ---
        for data in session_data:
            f.write(f"<a id=\"{data['session_link']}\"></a>\n")
            f.write(f"### {data['session_num']} - {data['formatted_date']} - {data['subject']}\n\n")
            f.write("[Back to Index](#session-index)\n\n")

            user_prompts = re.findall(r'\*\*User:\*\*\n(.*?)(?=\*\*Assistant:\*\*|\Z)', data['content'], re.DOTALL)
            assistant_responses = re.findall(r'\*\*Assistant:\*\*\n(.*?)(?=\*\*User:\*\*|\Z)', data['content'], re.DOTALL)

            for i, (user, ai) in enumerate(zip(user_prompts, assistant_responses)):
                sub_topic_num = f"{i+1:02d}"
                # Simple sub-topic extraction
                sub_topic_subject = user.strip().split('\n')[0]
                sub_topic_subject = (sub_topic_subject[:60] + '...') if len(sub_topic_subject) > 60 else sub_topic_subject
                sub_topic_link = f"{data['session_num']}-{sub_topic_num}"
                
                f.write(f"**{data['session_num']}-{sub_topic_num}** [{sub_topic_subject}](#{sub_topic_link})\n")

            f.write("\n")

            for i, (user, ai) in enumerate(zip(user_prompts, assistant_responses)):
                sub_topic_num = f"{i+1:02d}"
                sub_topic_subject = user.strip().split('\n')[0]
                sub_topic_subject = (sub_topic_subject[:60] + '...') if len(sub_topic_subject) > 60 else sub_topic_subject
                sub_topic_link = f"{data['session_num']}-{sub_topic_num}"

                f.write(f"<a id=\"{sub_topic_link}\"></a>\n")
                f.write(f"#### {data['session_num']}-{sub_topic_num} {sub_topic_subject}\n\n")
                f.write("**User:**\n")
                f.write(f"```\n{user.strip()}\n```\n\n")
                f.write("**AI:**\n")
                f.write(f"```\n{ai.strip()}\n```\n\n")

            f.write("\n---\n\n")

if __name__ == "__main__":
    summarize_claude_chats()
    print("Summary file 'Claude_Code_Chats_Summary.md' created successfully.")
