PROMPT 1 — PROJECT FOUNDATION
I want to build a real, full-stack biomedical web platform called BioNexsus.
I’m planning to use Next.js with the App Router, Tailwind CSS, FastAPI, PostgreSQL, and Firebase Authentication.
Can you help me set up a clean, production-ready project structure and explain how the frontend, backend, database, and authentication should work together?

PROMPT 2 — LANDING PAGE & PUBLIC CONTENT
I need a professional landing page for BioNexsus that feels trustworthy and suitable for a healthcare platform. 
It should clearly explain what the platform does,
how AI-based donor–recipient matching works, and include simple educational content about stem cells and donation, along with clear call-to-action buttons.

PROMPT 3 — AUTHENTICATION & USER ROLES
Help me set up Firebase email and password authentication. 
During signup, users should be able to choose whether
they’re a Patient, Donor, Hospital, Researcher, or Admin, and after login they should only be able to access features that make sense for their role.

PROMPT 4 — USER PROFILES & MEDICAL DATA
I want users to have proper profiles. Patients should be able to enter their medical needs and upload reports,
while Donors should enter health and eligibility details and give consent.This data needs to be stored securely and editable later.

PROMPT 5 — ROLE-BASED DASHBOARDS
Can you help me build dashboards based on user roles? Patients should see matched donors and request statuses, 
Donors should manage match requests and view their history, and Hospitals or Researchers should see anonymized match data and basic analytics.

PROMPT 6 — BACKEND APIs & DATABASE
I need a FastAPI backend with clean REST APIs and a PostgreSQL database to handle users, profiles, medical data, match requests, and dashboard data. 
Please include proper validation, authentication, and role-based access control.

PROMPT 7 — AI MATCHING SYSTEM (CORE FEATURE)
The core of this platform is AI-based matching. I want to match donors and recipients using medical attributes like blood group, age, and tissue compatibility. 
Please help me design this using XGBoost for compatibility scoring and KNN for similarity ranking, and explain how the final match scores are generated.

PROMPT 8 — FILE UPLOADS, SECURITY & COMPLIANCE
Medical data is sensitive, so I need secure file uploads for medical reports using Firebase Storage or S3. 
Along with that, I want basic healthcare-grade security like encryption, access logging, consent tracking, and controlled data access.

PROMPT 9 — ADMIN PANEL & MONITORING
I also need an admin area. Admins should be able to approve donors, verify hospitals, monitor matching activity, manage users, and keep an overall eye on how the platform is being used.

PROMPT 10 — NOTIFICATIONS & DEPLOYMENT
Finally, I want users to get email or in-app notifications when match requests or status updates happen,
and I want help preparing the whole project for production deployment, including environment variables, hosting, and a basic CI/CD setup.
