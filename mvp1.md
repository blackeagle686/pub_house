Software Requirements Specification — SRS
Project: Dar Al-Adib Publishing House

Project Name: Dar Al-Adib Publishing & Distribution Website
Organization: دار الأديب للنشر والتوزيع
Version: MVP v1.0
Architecture: Django Monolithic Web Application
Database: SQLite
Frontend: HTML5 + CSS3 + JavaScript + Bootstrap 5
Backend: Python + Django
Deployment Target: Linux / Python WSGI
Language: Arabic RTL — with architecture ready for English later

1. Project Overview
1.1 Purpose

The system is a web platform for دار الأديب للنشر والتوزيع that provides an online presence for the publishing house and allows visitors to:

Browse published books.
Search for books.
Explore authors.
View detailed book information.
Submit manuscripts for publishing consideration.
Contact the publishing house.
Read publishing-house news and announcements.

The system will also provide an administrative dashboard allowing authorized staff to manage books, authors, manuscripts, categories, news, and contact submissions.

2. MVP Goals

The MVP should accomplish five main goals:

                    DAR AL-ADIB
                         │
          ┌──────────────┼──────────────┐
          │              │              │
        Books          Authors       Publishing
          │              │           Submissions
          │              │              │
          └──────────────┼──────────────┘
                         │
                    Public Website
                         │
                    Admin Dashboard
Primary goals
Establish a professional online identity for the publishing house.
Present the publishing house's books in a searchable catalog.
Present authors and their published works.
Allow authors to submit manuscripts.
Give staff an easy CMS-like administration interface.
3. MVP Scope
Included
Public
Home page
About page
Books catalog
Book details
Authors catalog
Author details
Categories
Search
Manuscript submission
News / articles
Contact page
Responsive navigation
RTL Arabic UI
Administration
Authentication
Dashboard
Book management
Author management
Category management
Manuscript management
News management
Contact-message management
Basic statistics
Not Included in MVP

These should be Phase 2, not MVP:

Online payment
Shopping cart
Shipping integration
Inventory management
Customer accounts
Book reviews
Ratings
Advanced analytics
Mobile application
Recommendation engine
AI manuscript analysis
Multi-publisher support

This keeps the first version realistic.

4. User Roles
4.1 Visitor

Unauthenticated website user.

Can:

Browse books.
Search books.
Browse authors.
Read news.
Read about the publishing house.
Submit manuscript.
Send contact message.
4.2 Administrator

Full system access.

Can:

Manage books.
Manage authors.
Manage categories.
Manage manuscripts.
Manage news.
View contact messages.
Manage users through Django Admin.
View dashboard statistics.
4.3 Editor

Optional MVP role.

Can:

View submitted manuscripts.
Review manuscript information.
Change manuscript status.
Add internal notes.

Cannot:

Manage system users.
Change global settings.
5. Functional Requirements
FR-01 — Home Page

The system shall provide a professional homepage.

Sections
Header
   ↓
Hero Section
   ↓
Featured Books
   ↓
Latest Publications
   ↓
About Dar Al-Adib
   ↓
Featured Authors
   ↓
Publishing / Manuscript CTA
   ↓
Latest News
   ↓
Footer
Hero

Should contain:

Publishing house logo.
Short statement.
CTA button.

Example:

دار الأديب للنشر والتوزيع
نشر المعرفة ... نصنع الأثر

Buttons:

[استكشف الكتب]
[قدّم مخطوطتك]
FR-02 — Book Catalog

The system shall display all published books.

Each book card contains:

Cover
Title
Author
Category
Publication year
Short description
"View Details" button

Example:

┌────────────────────────┐
│                        │
│      BOOK COVER        │
│                        │
├────────────────────────┤
│ اسم الكتاب             │
│ اسم المؤلف             │
│ التصنيف                │
│                        │
│ [التفاصيل]             │
└────────────────────────┘
FR-03 — Book Search

Users shall be able to search books.

Search should support:

Book title
Author name
Category

Example:

بحث عن كتاب...
[ 🔍 ]

Django should process the search server-side.

For MVP:

Book.objects.filter(
    Q(title__icontains=query) |
    Q(author__name__icontains=query)
)
FR-04 — Book Details

Each book has a dedicated page.

Required information
Book cover
Title
Author
Category
Description
ISBN
Publisher
Publication date/year
Number of pages
Language
Format

Example:

┌──────────────┐
│              │
│    COVER     │
│              │
└──────────────┘

اسم الكتاب

تأليف: محمد أحمد

التصنيف: أدب

ISBN: XXXXXXXX

عدد الصفحات: 250

نبذة عن الكتاب
────────────────
...
FR-05 — Authors

The system shall provide an authors directory.

Each author:

Name
Profile image
Biography
Published books

Example:

Authors
 ├── Author A
 │    ├── Book 1
 │    └── Book 2
 │
 ├── Author B
 │    └── Book 3
 │
 └── Author C
FR-06 — Categories

Books shall belong to categories.

Example:

أدب
روايات
شعر
تاريخ
علوم
فكر
ثقافة
أطفال

Users can filter the catalog by category.

FR-07 — Manuscript Submission

This is one of the most important MVP features.

The website shall allow authors to submit manuscripts.

Form
Full Name *
Email *
Phone
Book Title *
Book Type *
Description *
Manuscript File *
Additional Notes
[ Submit ]

Supported file types initially:

PDF
DOC
DOCX
FR-08 — Manuscript Workflow

Each submission has a status.

SUBMITTED
    ↓
UNDER_REVIEW
    ↓
ACCEPTED
    ↓
REJECTED

Django model:

Manuscript
    |
    ├── title
    ├── author_name
    ├── email
    ├── phone
    ├── description
    ├── file
    ├── status
    ├── admin_notes
    ├── created_at
    └── updated_at

Admin can change the status.

FR-09 — News / Articles

The publishing house can publish news.

Each article contains:

Title
Cover image
Content
Author
Publication date
Status

Status:

Draft
Published

Public users can only see published articles.

FR-10 — Contact

Contact page contains:

Name *
Email *
Phone
Subject *
Message *

Submission is saved in database.

Admin can view messages from dashboard.

FR-11 — About Us

Static page describing:

Dar Al-Adib
Mission
Vision
Publishing philosophy
Contact information
FR-12 — Admin Dashboard

Dashboard should provide a high-level overview.

Example:

┌─────────────────────────────────────────┐
│             Dashboard                   │
├───────────┬───────────┬─────────────────┤
│   Books   │  Authors  │  Manuscripts    │
│    124    │    56     │       18        │
├───────────┴───────────┴─────────────────┤
│                                         │
│ Pending Manuscripts: 7                  │
│ New Messages: 12                        │
│ Published News: 24                      │
│                                         │
└─────────────────────────────────────────┘
6. Database Design

For MVP, SQLite is completely sufficient.

Entity Relationship
                    Category
                       │
                       │ 1:N
                       ↓
Author ────────────→ Book
  │                   │
  │                   │
  │                   │
  └─────── N:M ───────┘

Manuscript

NewsArticle

ContactMessage

User
7. Django Models
Author
class Author(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    biography = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to="authors/",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
Category
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
Book
class Book(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books"
    )

    description = models.TextField()

    cover = models.ImageField(
        upload_to="books/"
    )

    isbn = models.CharField(
        max_length=20,
        blank=True
    )

    publication_year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    pages = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    language = models.CharField(
        max_length=50,
        default="العربية"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
Manuscript
class Manuscript(models.Model):

    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("reviewing", "Under Review"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    author_name = models.CharField(max_length=200)

    email = models.EmailField()

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField()

    file = models.FileField(
        upload_to="manuscripts/"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="submitted"
    )

    admin_notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
NewsArticle
class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    content = models.TextField()

    image = models.ImageField(
        upload_to="news/",
        blank=True,
        null=True
    )

    published = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
ContactMessage
class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    subject = models.CharField(
        max_length=255
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
8. Project Architecture

Since this is Django, I'd avoid putting the entire project into one giant app.

Use:

dar_al_adib/
│
├── manage.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   │
│   ├── books/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   └── admin.py
│   │
│   ├── authors/
│   │
│   ├── manuscripts/
│   │
│   ├── news/
│   │
│   └── core/
│
├── templates/
│   ├── base.html
│   │
│   ├── home/
│   ├── books/
│   ├── authors/
│   ├── manuscripts/
│   ├── news/
│   └── core/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/
│   ├── books/
│   ├── authors/
│   ├── manuscripts/
│   └── news/
│
└── db.sqlite3
9. Frontend Requirements
Framework

Use:

HTML5
CSS3
Bootstrap 5
Vanilla JavaScript

No React/Next/Vue required.

The project is primarily server-rendered Django templates.

10. Design Requirements

The design should preserve the identity of the existing logo:

Main colors
Gold
#D4A017

Dark Gold
#9C6B00

Black
#111111

Orange
#F59E0B

Cream
#FFF8E7

Use the gold/black/orange combination carefully rather than making the entire website gold.

Recommended visual hierarchy
White / Cream
     ↓
Dark text
     ↓
Gold accents
     ↓
Orange highlights
     ↓
Black sections
11. Navbar

Desktop:

[LOGO]

الرئيسية
الكتب
المؤلفون
عن الدار
الأخبار
قدّم مخطوطتك
تواصل معنا

Mobile:

[LOGO]                 ☰

Navbar should remain responsive through Bootstrap.

12. Homepage UX

Recommended structure:

┌───────────────────────────────────────────┐
│ NAVBAR                                    │
├───────────────────────────────────────────┤
│                                           │
│              HERO                         │
│       دار الأديب للنشر والتوزيع            │
│      نشر المعرفة ... نصنع الأثر            │
│                                           │
│     [ استكشف الكتب ] [ قدّم مخطوطتك ]      │
│                                           │
├───────────────────────────────────────────┤
│             أحدث الإصدارات                │
│                                           │
│     📕       📕       📕       📕         │
│                                           │
├───────────────────────────────────────────┤
│              عن دار الأديب                │
├───────────────────────────────────────────┤
│              مؤلفونا                      │
├───────────────────────────────────────────┤
│             لماذا الأديب؟                 │
├───────────────────────────────────────────┤
│               الأخبار                     │
├───────────────────────────────────────────┤
│               CTA                         │
│       هل لديك مخطوطة؟                    │
│          [أرسل مخطوطتك]                  │
├───────────────────────────────────────────┤
│ FOOTER                                    │
└───────────────────────────────────────────┘
13. URL Structure

Keep URLs clean and SEO-friendly.

/
 /books/
/books/<slug>/

/authors/
/authors/<slug>/

/categories/<slug>/

/news/
/news/<slug>/

/about/

/manuscript/submit/

/contact/

Admin:

/admin/
14. SEO Requirements

Every book should have:

<title>
<meta name="description">
<meta name="keywords">
Open Graph metadata
Canonical URL

Example:

دار الأديب للنشر والتوزيع | اسم الكتاب

Use semantic HTML:

<header>
<nav>
<main>
<section>
<article>
<footer>
15. Security Requirements

Django security mechanisms must remain enabled.

Required
CSRF protection.
Django authentication.
Password hashing.
Permission checks.
File upload validation.
Maximum upload size.
Allowed file extensions.
Secure production settings.
Environment variables for secrets.

Especially for manuscripts:

DO NOT trust uploaded filenames.
DO NOT allow arbitrary executable files.
16. File Upload Requirements

Manuscripts:

.pdf
.doc
.docx

Book covers:

.jpg
.jpeg
.png
.webp

Maximum manuscript size for MVP:

10 MB

Can be increased later.

17. Admin Requirements

Django Admin should be customized rather than using the raw default experience.

Example:

Dashboard

Books
 ├── All Books
 ├── Add Book
 └── Categories

Authors
 ├── All Authors
 └── Add Author

Manuscripts
 ├── New
 ├── Under Review
 ├── Accepted
 └── Rejected

News
 ├── Published
 └── Drafts

Messages
 ├── Unread
 └── Read
18. Performance Requirements

For MVP:

Server-side rendering.
Bootstrap CDN or locally hosted assets.
Optimized images.
Pagination for books/news.
Django ORM.
select_related() for book → author/category queries.
Avoid unnecessary database queries.

Example:

Book.objects.select_related(
    "author",
    "category"
)
19. Pagination

Books:

12 books/page

News:

6 articles/page

Authors:

12 authors/page

Can be changed later.

20. Error Handling

Required pages:

404.html
500.html
403.html

User-friendly Arabic messages.

Example:

عذرًا، الصفحة التي تبحث عنها غير موجودة.

21. Testing Requirements

Minimum testing:

Models
Book creation.
Author creation.
Category relationship.
Manuscript creation.
Views
Homepage.
Book listing.
Book details.
Author details.
Search.
Manuscript submission.
Contact submission.
Security
Unauthorized admin access.
Invalid manuscript file.
CSRF.
Invalid form submissions.
22. MVP Acceptance Criteria

The MVP is considered complete when:

Public Website
 Homepage works.
 Website is responsive.
 RTL works correctly.
 Logo is integrated.
 Books can be browsed.
 Books can be searched.
 Book details work.
 Authors can be browsed.
 Author details work.
 Categories work.
 News works.
 Contact form works.
 Manuscript submission works.
Admin
 Admin authentication works.
 Admin can create books.
 Admin can edit books.
 Admin can delete books.
 Admin can create authors.
 Admin can manage categories.
 Admin can review manuscripts.
 Admin can change manuscript status.
 Admin can publish news.
 Admin can view contact messages.
Technical
 SQLite database works.
 Media uploads work.
 Static files work.
 CSRF enabled.
 File validation enabled.
 404/500 pages implemented.
 Basic automated tests implemented.
23. Development Phases

أنا أقترح نمشي بالترتيب ده بدل ما نفتح كل حاجة مرة واحدة:

Phase 1 — Foundation
Django setup
Settings
Apps
SQLite
Static
Media
Base template
Bootstrap
RTL
Phase 2 — Core Content
Authors
Categories
Books
Book details
Search
Phase 3 — Public Website
Homepage
About
Authors
Books
News
Contact
Footer
Responsive UI
Phase 4 — Publishing
Manuscript model
Upload
Submission form
Admin review
Status workflow
Phase 5 — Admin
Django Admin customization
Dashboard
Filters
Search
Actions
Phase 6 — Polish
SEO
404
500
Security
Image optimization
Testing
Mobile UX
Deployment
24. Future Architecture

المهم هنا إننا ما نعملش MVP بشكل يقفلنا بعدين.

الـ architecture تكون قابلة للتوسع:

                    DAR AL-ADIB
                         │
              ┌──────────┴──────────┐
              │                     │
          Public Site           Admin
              │                     │
              └──────────┬──────────┘
                         │
                      Django
                         │
        ┌────────────────┼────────────────┐
        │                │                │
      Books           Publishing       Content
        │              Workflow           │
        │                │                │
        └────────────────┼────────────────┘
                         │
                       DB
                         │
                     SQLite

ثم في V2/V3:

SQLite
   ↓
PostgreSQL

Local Media
   ↓
S3 / Cloud Storage

Simple Search
   ↓
PostgreSQL Full Text / Elasticsearch

No Payments
   ↓
Payment Gateway

No Orders
   ↓
E-Commerce

Simple Manuscript Workflow
   ↓
Full Editorial Management
25. Final MVP Stack
┌─────────────────────────────────┐
│           Frontend              │
│ HTML5 + CSS3 + Bootstrap 5      │
│ Vanilla JavaScript              │
└───────────────┬─────────────────┘
                │
                ↓
┌─────────────────────────────────┐
│             Django              │
│                                 │
│ Views                           │
│ Forms                           │
│ Models                          │
│ Authentication                  │
│ Django Admin                    │
│ Templates                       │
└───────────────┬─────────────────┘
                │
                ↓
┌─────────────────────────────────┐
│             SQLite              │
└─────────────────────────────────┘

Media → Book Covers / Author Photos /
         Manuscripts / News Images
أهم قرار في الـ MVP

ما نعملش متجر دلوقتي.

الـ MVP يكون Professional Publishing House Website + Publishing Management Portal.

وده يخلي المشروع صغير بما يكفي يتعمل بسرعة، وفي نفس الوقت فيه حاجات Backend حقيقية: relational modeling + file uploads + authentication + permissions + workflows + search + CMS + admin operations.

ولو هنبدأ التنفيذ بعد الـ SRS، فأنا هبدأ بالـ Django project structure + models + URLs + templates architecture الأول، وبعدها نمسك الـ Homepage والـ Book Catalog ونبنيهم فوق الـ foundation بدل ما نبدأ بالـ UI عشوائي.