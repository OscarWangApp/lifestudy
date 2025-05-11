from models.achievement_model import create_achievement_table, add_achievement, delete_achievement
from models.database import get_db

def init_achievements():
    """Initialize the achievement table and add sample achievements."""
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Start transaction
        cursor.execute("BEGIN")
        
        # Create achievement table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS achievement_info (
                code VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                `condition` TEXT NOT NULL,
                encouragement TEXT NOT NULL
            )
        """)
        
        # Clear existing achievements
        cursor.execute("DELETE FROM achievement_info")
        
        # Sample achievements
        achievements = [
            {
                'code': '00001',
                'name': 'First Chapter',
                'condition': 'Σ(chapters_completed) = 1',
                'encouragement': 'Great start! Your journey begins with a single step.'
            },
            {
                'code': '00005',
                'name': 'Five Chapters',
                'condition': 'Σ(chapters_completed) = 5',
                'encouragement': 'You\'ve completed five chapters! Keep up the good work.'
            },
            {
                'code': '00010',
                'name': 'Ten Chapters',
                'condition': 'Σ(chapters_completed) = 10',
                'encouragement': 'Double digits! Your dedication is growing.'
            },
            {
                'code': '00050',
                'name': 'Fifty Chapters',
                'condition': 'Σ(chapters_completed) = 50',
                'encouragement': 'Half a century of chapters! Your commitment is impressive.'
            },
            {
                'code': '00100',
                'name': 'Century Mark',
                'condition': 'Σ(chapters_completed) = 100',
                'encouragement': 'A century of chapters! You\'re making remarkable progress.'
            },
            {
                'code': '00150',
                'name': '150 Chapters',
                'condition': 'Σ(chapters_completed) = 150',
                'encouragement': '150 chapters and counting! Your perseverance is inspiring.'
            },
            {
                'code': '00200',
                'name': '200 Chapters',
                'condition': 'Σ(chapters_completed) = 200',
                'encouragement': '200 chapters! You\'re building a strong foundation.'
            },
            {
                'code': '00250',
                'name': '250 Chapters',
                'condition': 'Σ(chapters_completed) = 250',
                'encouragement': '250 chapters completed! Your dedication is unwavering.'
            },
            {
                'code': '00300',
                'name': '300 Chapters',
                'condition': 'Σ(chapters_completed) = 300',
                'encouragement': '300 chapters! You\'re making steady progress.'
            },
            {
                'code': '00350',
                'name': '350 Chapters',
                'condition': 'Σ(chapters_completed) = 350',
                'encouragement': '350 chapters and still going strong!'
            },
            {
                'code': '00400',
                'name': '400 Chapters',
                'condition': 'Σ(chapters_completed) = 400',
                'encouragement': '400 chapters! Your journey is flourishing.'
            },
            {
                'code': '00450',
                'name': '450 Chapters',
                'condition': 'Σ(chapters_completed) = 450',
                'encouragement': '450 chapters completed! Your dedication is remarkable.'
            },
            {
                'code': '00500',
                'name': '500 Chapters',
                'condition': 'Σ(chapters_completed) = 500',
                'encouragement': 'Half a thousand chapters! What an achievement!'
            },
            {
                'code': '00550',
                'name': '550 Chapters',
                'condition': 'Σ(chapters_completed) = 550',
                'encouragement': '550 chapters! Your spiritual journey is deepening.'
            },
            {
                'code': '00600',
                'name': '600 Chapters',
                'condition': 'Σ(chapters_completed) = 600',
                'encouragement': '600 chapters! You\'re making incredible progress.'
            },
            {
                'code': '00650',
                'name': '650 Chapters',
                'condition': 'Σ(chapters_completed) = 650',
                'encouragement': '650 chapters completed! Your commitment is inspiring.'
            },
            {
                'code': '00700',
                'name': '700 Chapters',
                'condition': 'Σ(chapters_completed) = 700',
                'encouragement': '700 chapters! You\'re building a legacy of learning.'
            },
            {
                'code': '00750',
                'name': '750 Chapters',
                'condition': 'Σ(chapters_completed) = 750',
                'encouragement': '750 chapters! Your dedication knows no bounds.'
            },
            {
                'code': '00800',
                'name': '800 Chapters',
                'condition': 'Σ(chapters_completed) = 800',
                'encouragement': '800 chapters! You\'re approaching the finish line.'
            },
            {
                'code': '00850',
                'name': '850 Chapters',
                'condition': 'Σ(chapters_completed) = 850',
                'encouragement': '850 chapters! The end is in sight.'
            },
            {
                'code': '00900',
                'name': '900 Chapters',
                'condition': 'Σ(chapters_completed) = 900',
                'encouragement': '900 chapters! You\'re in the final stretch.'
            },
            {
                'code': '00950',
                'name': '950 Chapters',
                'condition': 'Σ(chapters_completed) = 950',
                'encouragement': '950 chapters! Almost there!'
            },
            {
                'code': '01000',
                'name': 'Thousand Chapters',
                'condition': 'Σ(chapters_completed) = 1000',
                'encouragement': 'A thousand chapters! What an incredible milestone!'
            },
            {
                'code': '01050',
                'name': '1050 Chapters',
                'condition': 'Σ(chapters_completed) = 1050',
                'encouragement': '1050 chapters! Your journey continues.'
            },
            {
                'code': '01100',
                'name': '1100 Chapters',
                'condition': 'Σ(chapters_completed) = 1100',
                'encouragement': '1100 chapters! You\'re making great progress.'
            },
            {
                'code': '01150',
                'name': '1150 Chapters',
                'condition': 'Σ(chapters_completed) = 1150',
                'encouragement': '1150 chapters! Your dedication is unwavering.'
            },
            {
                'code': '01200',
                'name': '1200 Chapters',
                'condition': 'Σ(chapters_completed) = 1200',
                'encouragement': '1200 chapters! You\'re building a strong foundation.'
            },
            {
                'code': '01250',
                'name': '1250 Chapters',
                'condition': 'Σ(chapters_completed) = 1250',
                'encouragement': '1250 chapters! Your journey is flourishing.'
            },
            {
                'code': '01300',
                'name': '1300 Chapters',
                'condition': 'Σ(chapters_completed) = 1300',
                'encouragement': '1300 chapters! Your commitment is inspiring.'
            },
            {
                'code': '01350',
                'name': '1350 Chapters',
                'condition': 'Σ(chapters_completed) = 1350',
                'encouragement': '1350 chapters! You\'re making steady progress.'
            },
            {
                'code': '01400',
                'name': '1400 Chapters',
                'condition': 'Σ(chapters_completed) = 1400',
                'encouragement': '1400 chapters! Your dedication is remarkable.'
            },
            {
                'code': '01450',
                'name': '1450 Chapters',
                'condition': 'Σ(chapters_completed) = 1450',
                'encouragement': '1450 chapters! You\'re approaching the finish line.'
            },
            {
                'code': '01500',
                'name': '1500 Chapters',
                'condition': 'Σ(chapters_completed) = 1500',
                'encouragement': '1500 chapters! The end is in sight.'
            },
            {
                'code': '01550',
                'name': '1550 Chapters',
                'condition': 'Σ(chapters_completed) = 1550',
                'encouragement': '1550 chapters! You\'re in the final stretch.'
            },
            {
                'code': '01600',
                'name': '1600 Chapters',
                'condition': 'Σ(chapters_completed) = 1600',
                'encouragement': '1600 chapters! Almost there!'
            },
            {
                'code': '01650',
                'name': '1650 Chapters',
                'condition': 'Σ(chapters_completed) = 1650',
                'encouragement': '1650 chapters! Your journey continues.'
            },
            {
                'code': '01700',
                'name': '1700 Chapters',
                'condition': 'Σ(chapters_completed) = 1700',
                'encouragement': '1700 chapters! You\'re making great progress.'
            },
            {
                'code': '01750',
                'name': '1750 Chapters',
                'condition': 'Σ(chapters_completed) = 1750',
                'encouragement': '1750 chapters! Your dedication is unwavering.'
            },
            {
                'code': '01800',
                'name': '1800 Chapters',
                'condition': 'Σ(chapters_completed) = 1800',
                'encouragement': '1800 chapters! You\'re building a strong foundation.'
            },
            {
                'code': '01850',
                'name': '1850 Chapters',
                'condition': 'Σ(chapters_completed) = 1850',
                'encouragement': '1850 chapters! Your journey is flourishing.'
            },
            {
                'code': '01900',
                'name': '1900 Chapters',
                'condition': 'Σ(chapters_completed) = 1900',
                'encouragement': '1900 chapters! Your commitment is inspiring.'
            },
            {
                'code': '01950',
                'name': '1950 Chapters',
                'condition': 'Σ(chapters_completed) = 1950',
                'encouragement': '1950 chapters! You\'re making steady progress.'
            },
            {
                'code': '01984',
                'name': 'Complete Journey',
                'condition': 'Σ(chapters_completed) = 1984',
                'encouragement': 'Congratulations! You have completed all 1984 chapters! What an incredible achievement!'
            }
        ]
        
        # Add sample achievements
        for achievement in achievements:
            cursor.execute("""
                INSERT INTO achievement_info (code, name, `condition`, encouragement)
                VALUES (%s, %s, %s, %s)
            """, (
                achievement['code'],
                achievement['name'],
                achievement['condition'],
                achievement['encouragement']
            ))
        
        # Commit transaction
        db.commit()
        print("Successfully initialized achievements")
        
    except Exception as e:
        print(f"Error initializing achievements: {e}")
        db.rollback()
    finally:
        cursor.close()
        db.close()

if __name__ == "__main__":
    init_achievements() 