import argparse
from app.database import SessionLocal
from app.utility_digitilization.utils.seeding.seed_utility import seed_all as seed_utility_accounts


def seed_all(env: str):
    """
    Seed database with all project data.
    :param env: Environment (development or production)
    :return:
    """
    with SessionLocal() as db:
        try:
            seed_utility_accounts(db, env)
            db.commit()
            print("Database seeding completed successfully!")
        except Exception as e:
            db.rollback()
            print(f"Database seeding failed: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed the database")
    parser.add_argument("--env", type=str, help="Environment (development or production)", default="development")
    args = parser.parse_args()

    seed_all(env=args.env)
