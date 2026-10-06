"""
Structured education, work experience, and leadership data.
Extracted and verified against Mithilesh Chaurasiya's official resume and academic records.
"""

EXPERIENCE = [
    {
        "company": "Infosys Ltd.",
        "role": "Senior System Associate (Data Engineering & ETL Testing)",
        "period": "June 2021 – January 2024",
        "duration": "2.8 Years",
        "location": "India",
        "summary": (
            "Engineered and validated production-ready data pipelines and ML systems through rigorous "
            "ETL testing, automated data validation, and MLOps tooling adoption across cross-functional enterprise teams."
        ),
        "highlights": [
            "Validated and monitored production-grade ETL pipelines handling large-scale structured data across Oracle, MongoDB, and Snowflake, ensuring high data integrity for downstream ML and analytics systems.",
            "Built Python-based automation frameworks for data validation and API testing, reducing manual QA effort by 30%+ and improving overall pipeline reliability.",
            "Optimized ETL workflows to generate ML-ready datasets, accelerating data preparation and feature extraction for analytics models.",
            "Performed end-to-end validation of REST APIs and model endpoints using Postman and Python, ensuring correctness of model outputs in integrated production systems.",
            "Collaborated with cross-functional engineering teams to introduce MLflow experiment tracking and DVC dataset versioning, establishing reproducible model development workflows.",
            "Contributed to Agile/Scrum sprints as part of an 8-member engineering team, delivering 15+ sprint features on schedule with robust test automation."
        ],
        "technologies": ["Python", "SQL (Oracle)", "MongoDB", "Snowflake", "Apache Spark", "Selenium", "Postman", "MLflow", "DVC", "Azure DevOps", "Jenkins"]
    }
]

LEADERSHIP = [
    {
        "role": "Machine Learning Team Lead",
        "organization": "Developers and Coders Club (DCC)",
        "institution": "National Institute of Technology, Agartala",
        "period": "2024 – Present",
        "responsibilities": [
            "Lead the institute's Machine Learning team, mentoring students on applied ML, Deep Learning, and Computer Vision.",
            "Conduct structured workshops on ML fundamentals, end-to-end vision pipelines (OpenCV/YOLO), and MLOps best practices.",
            "Guide student project teams on building production-oriented AI systems, Kaggle problem-solving, and deployment architectures.",
            "Coordinate with faculty mentors to design technical roadmaps and applied machine learning initiatives."
        ]
    }
]

EDUCATION = [
    {
        "degree": "Master of Computer Application (MCA)",
        "status": "Pursuing",
        "institution": "National Institute of Technology, Agartala",
        "location": "Agartala, Tripura, India",
        "period": "2024 – Expected 2027",
        "details": "Specializing in Machine Learning, Computer Vision, and Distributed Systems. Leading DCC ML team."
    },
    {
        "degree": "Bachelor of Science in Computer Science (B.Sc. CS)",
        "status": "Completed",
        "institution": "Thakur College of Science & Commerce",
        "location": "Mumbai, Maharashtra, India",
        "period": "2018 – 2021",
        "details": "Graduated with CGPA 8.87 / 10. Core coursework in Data Structures, Algorithms, DBMS, and Software Engineering."
    },
    {
        "degree": "Higher Secondary Certificate (HSC / 12th)",
        "status": "Completed",
        "institution": "Utkarsha Vidyalaya & Junior College",
        "location": "Mumbai, Maharashtra, India",
        "period": "2016 – 2018",
        "details": "Science Stream. Percentage: 64%."
    },
    {
        "degree": "Secondary School Certificate (SSC / 10th)",
        "status": "Completed",
        "institution": "Jai Deep Vidya Mandir High School",
        "location": "Mumbai, Maharashtra, India",
        "period": "2006 – 2016",
        "details": "Percentage: 75%."
    }
]
