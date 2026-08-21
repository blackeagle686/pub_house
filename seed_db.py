import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.authors.models import Author
from apps.books.models import Category, Book
from apps.news.models import NewsArticle

def seed():
    # 1. Categories
    categories_data = [
        ("روايات", "novel"),
        ("شعر", "poetry"),
        ("تاريخ", "history"),
        ("فكر إسلامي", "islamic-thought"),
        ("تنمية ذاتية", "self-development"),
        ("أدب عالمي مترجم", "translated-literature"),
    ]
    
    categories = {}
    for name, slug in categories_data:
        cat, _ = Category.objects.get_or_create(name=name, slug=slug)
        categories[slug] = cat

    # 2. Authors
    authors_data = [
        ("د. سيد غيث", "sayed-ghaith", "الكاتب والشاعر مؤسس دار الأديب للطبع والنشر والتوزيع. له العديد من الإسهامات في إثراء الحركة الثقافية والأدبية في مصر والعالم العربي."),
        ("نجيب محفوظ", "naguib-mahfouz", "روائي مصري وأول عربي حائز على جائزة نوبل في الأدب. تُعد أعماله مرآة للحياة الاجتماعية والسياسية في مصر."),
        ("أحمد خالد توفيق", "ahmed-khaled-tawfik", "طبيب وأديب مصري، ويعتبر من رواد أدب الرعب والفانتازيا والخيال العلمي في الوطن العربي."),
        ("محمود درويش", "mahmoud-darwish", "أحد أهم الشعراء الفلسطينيين والعرب الذين ارتبط اسمهم بشعر الثورة والوطن.")
    ]
    
    authors = {}
    for name, slug, bio in authors_data:
        auth, _ = Author.objects.get_or_create(name=name, slug=slug, defaults={"biography": bio})
        authors[slug] = auth

    # 3. Books
    books_data = [
        {
            "title": "أولاد حارتنا",
            "slug": "awlad-haretna",
            "author": authors["naguib-mahfouz"],
            "category": categories["novel"],
            "description": "من أشهر روايات نجيب محفوظ وأكثرها إثارة للجدل، ترمز إلى تاريخ البشرية وصراع الإنسان المستمر مع السلطة والظلم بحثاً عن العدالة المثالية.",
            "isbn": "978-977-09-1466-2",
            "publication_year": 1959,
            "pages": 580
        },
        {
            "title": "يوتوبيا",
            "slug": "utopia",
            "author": authors["ahmed-khaled-tawfik"],
            "category": categories["novel"],
            "description": "رواية تدور أحداثها في عام 2023 حيث تحولت مصر إلى طبقتين، الأولى بالغة الثراء تعيش في مجتمع مغلق (يوتوبيا)، والثانية تعيش في فقر مدقع.",
            "isbn": "978-977-14-4113-6",
            "publication_year": 2008,
            "pages": 192
        },
        {
            "title": "في حضرة الغياب",
            "slug": "fi-hadrat-al-ghiyab",
            "author": authors["mahmoud-darwish"],
            "category": categories["poetry"],
            "description": "نص نثري طويل يروي فيه الشاعر محمود درويش سيرته الذاتية وتأملاته في الحياة والموت، بلغة شعرية مكثفة وفلسفية عميقة.",
            "isbn": "978-9953-89-106-9",
            "publication_year": 2006,
            "pages": 240
        },
        {
            "title": "خواطر أدبية",
            "slug": "khawater-adabeya",
            "author": authors["sayed-ghaith"],
            "category": categories["novel"],
            "description": "مجموعة من الخواطر والقصائد النثرية التي تلامس الروح والعقل للمفكر والشاعر د. سيد غيث، تعكس تجاربه في الحياة ورؤيته للمستقبل.",
            "isbn": "978-000-00-0000-0",
            "publication_year": 2025,
            "pages": 150
        },
        {
            "title": "الحرافيش",
            "slug": "al-harafish",
            "author": authors["naguib-mahfouz"],
            "category": categories["novel"],
            "description": "ملحمة روائية تسرد قصة أجيال متعاقبة من عائلة عاشور الناجي، وكيف تتقلب بهم الحياة بين القوة والضعف، العدل والظلم.",
            "isbn": "978-977-09-2134-9",
            "publication_year": 1977,
            "pages": 450
        }
    ]

    for b_data in books_data:
        Book.objects.get_or_create(slug=b_data["slug"], defaults=b_data)
        
    # 4. News
    NewsArticle.objects.get_or_create(
        slug="book-fair-2026",
        defaults={
            "title": "مشاركة دار الأديب في معرض القاهرة الدولي للكتاب 2026",
            "content": "تستعد دار الأديب للطبع والنشر للمشاركة في الدورة القادمة من معرض القاهرة الدولي للكتاب بمجموعة مميزة من الإصدارات الجديدة التي تناسب كافة الأذواق، وسيكون هناك حفل توقيع للعديد من الكتاب الشباب.",
            "published": True
        }
    )

    print("Database seeded successfully with Arabic data!")

if __name__ == '__main__':
    seed()
