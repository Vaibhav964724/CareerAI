def test_api_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_api_student_lifecycle(client):
    # 1. Create student
    payload = {
        "name": "Dev Sharma",
        "email": "dev@college.edu",
        "degree": "B.Tech Computer Science",
        "branch": "CSE",
        "year_of_study": 3,
        "gpa": 8.1,
        "interests": ["Data Science", "Python"],
        "existing_projects": ["Student DB"],
        "completed_certifications": [],
        "target_role": "Data Analyst",
        "preferred_industry": "Finance",
        "weekly_hours": 10.0,
        "timeline_months": 6,
        "skills": [
            {"skill_name": "Python", "proficiency": 2},
            {"skill_name": "SQL", "proficiency": 2}
        ]
    }
    create_res = client.post("/api/v1/students", json=payload)
    assert create_res.status_code == 201
    student_data = create_res.json()
    student_id = student_data["id"]
    assert student_data["name"] == "Dev Sharma"

    # 2. Get student
    get_res = client.get(f"/api/v1/students/{student_id}")
    assert get_res.status_code == 200
    assert len(get_res.json()["skills"]) == 2

    # 3. Analyze skill gaps
    gap_res = client.post("/api/v1/careers/skill-gaps", json={
        "student_id": student_id,
        "target_role": "Data Analyst"
    })
    assert gap_res.status_code == 200
    gap_data = gap_res.json()
    assert gap_data["target_role"] == "Data Analyst"
    assert len(gap_data["gaps"]) > 0

    # 4. Generate roadmap
    rm_res = client.post("/api/v1/roadmaps/generate", json={
        "student_id": student_id,
        "target_role": "Data Analyst",
        "weekly_hours": 10.0
    })
    assert rm_res.status_code == 201
    rm_data = rm_res.json()
    assert len(rm_data["milestones"]) > 0
    first_milestone_id = rm_data["milestones"][0]["id"]

    # 5. Update milestone status
    patch_res = client.patch(f"/api/v1/roadmaps/milestones/{first_milestone_id}", json={
        "new_status": "in_progress",
        "notes": "Starting practical exercises"
    })
    assert patch_res.status_code == 200
    assert patch_res.json()["new_status"] == "in_progress"

    # 6. Trigger agent evaluation
    agent_res = client.post(f"/api/v1/agent/evaluate/{student_id}", json={
        "trigger": "test_verification"
    })
    assert agent_res.status_code == 200
    eval_data = agent_res.json()
    assert eval_data["cycle_status"] == "completed"

    # 7. Ask Career Assistant a question
    chat_res = client.post("/api/v1/assistant/chat", json={
        "student_id": student_id,
        "message": "What should I learn this week?"
    })
    assert chat_res.status_code == 200
    chat_data = chat_res.json()
    assert "reply" in chat_data
    assert len(chat_data["reply"]) > 20
    assert chat_data["mode"] in ["rule-based", "llm"]
