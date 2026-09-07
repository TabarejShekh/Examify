<h1 align="center">🎓 Examify - Online Examination Management System</h1>

<p align="center">
  <em>A modern, scalable, and secure platform for academic assessments, built with Django.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Django-4.x-092E20.svg?logo=django" alt="Django Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

---

## 📖 About the Project

**Examify** is a comprehensive full-stack Online Examination Management System designed specifically for modern academic institutions. It bridges the gap between traditional examinations and digital convenience, offering highly secure, intuitive, and feature-rich portals for both educators and students.

Developed with a focus on **integrity**, **speed**, and **user experience**, Examify introduces a modern *glassmorphic* design integrated with powerful backend logic to streamline result generation and examination management.

## ✨ Key Features

### 🛡️ For Examination Integrity & Proctoring
*   **Behavior Tracking**: Tracks user tab-switching and loss of focus during the exam to curb cheating.
*   **Strict UI Lockdowns**: Disables copy, paste, right-click context menus, and inspect element tools during the examination.
*   **Full-Screen Enforcement**: Requires candidates to take exams in full-screen mode for maximum focus.

### 👩‍🏫 For Teachers & Administrators
*   **Rapid Quiz Generation**: The innovative **Fast Paste Parser** allows teachers to bulk-upload questions near-instantly, bypassing tedious manual entry.
*   **Advanced Marking Options**: Supports complex grading structures including custom fractional negative marking.
*   **Jazzmin Admin Panel**: A beautifully styled, sleek backend control center to manage students, courses, exams, and results.
*   **Result Analytics**: Instant, automated evaluation and structured result reporting across departments.

### 👨‍🎓 For Students
*   **Next-Gen UI/UX**: A responsive, glassmorphism-inspired interface that ensures a premium test-taking experience.
*   **Smart Registration**: Features live profile picture preview and dynamic department selection.
*   **Rule-Based Chatbot**: An integrated, 24/7 AI-assistant to help resolve common portal issues, commands, and FAQs instantly.
*   **Instant Result Tracking**: View past examination records, scorecards, and performance history immediately after submission.

---

## 🛠️ Technology Stack

*   **Backend**: Python, Django
*   **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism UI), JavaScript
*   **Database**: SQLite (Development) / Ready for PostgreSQL (Production)
*   **Admin Dashboard**: Django-Jazzmin
*   **Architecture**: MVT (Model-View-Template)

---

## 🚀 Installation & Local Setup

Follow these steps to run Examify locally on your machine.

### Prerequisites
* Python 3.10 or higher installed.
* `pip` and `virtualenv` installed.

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/Examify.git
   cd Examify
   ```

2. **Create and Activate a Virtual Environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Database Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   # Follow the prompts to set your email, username, and password
   ```

6. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Platform**
   * **Main Site**: `http://127.0.0.1:8000/`
   * **Admin Panel**: `http://127.0.0.1:8000/admin/`

---

## 📸 Screenshots
*(Recommended: Add screenshots of your project here by uploading them to the repository and linking them)*

* **Home Page**: `![Home](docs/images/home.png)`
* **Student Dashboard**: `![Student UI](docs/images/student.png)`
* **Exam Interface**: `![Exam](docs/images/exam.png)`
* **Jazzmin Admin Panel**: `![Admin](docs/images/admin.png)`

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/Examify/issues).

## 📝 License
This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.

<br>
<p align="center">Made with ❤️ by <b>Mohd Sarim Khan</b></p>
