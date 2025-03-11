from utils import clean_text

def generate_email(job_info, portfolio_df, user_name, user_role):
    """Generates a cold email using cleaned job details, user info, and portfolio."""
    
    role = clean_text(job_info.get("role", "Software Engineer"))
    company = clean_text(job_info.get("company", "Company"))
    skills = clean_text(job_info.get("skills", "relevant skills"))
    
    # Find matching projects
    matching_projects = []
    for _, row in portfolio_df.iterrows():
        tech_stack = clean_text(row["Techstack"])
        if any(skill.lower() in tech_stack.lower() for skill in skills.split(", ")):
            matching_projects.append((tech_stack, row["Links"]))
    
    # Format matching projects
    project_details = "\n".join([f"- {proj[0]}: {proj[1]}" for proj in matching_projects]) or "No direct project matches, but I am eager to apply my skills to this role!"

    # Email Template
    email = f"""
    Subject: Excited to Apply for {role} at {company}
    
    Dear Hiring Manager,
    
    I hope you’re doing well! My name is {user_name}, and I am a {user_role}. 
    I came across the {role} position at {company} and was excited to learn more about the opportunity.
    
    With my experience in {skills}, I believe I could be a strong fit for your team. 
    Here are some projects where I applied these skills:
    
    {project_details}
    
    I would love to discuss how my experience aligns with your team’s needs. Looking forward to hearing from you!
    
    Best Regards,  
    {user_name}  
    {user_role}
    """
    
    return email
