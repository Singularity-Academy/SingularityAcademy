import sys
import os
import asyncio

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_engine.apps.principal.course import generate_course_outline

sample_course = {
    "name": "Introduction to Artificial Intelligence",
    "description": "A foundational course covering the basics of AI, including search, logic, machine learning, and applications. Suitable for beginners with basic programming knowledge."
}

async def main():
    print("Generating course outline for test course...")
    try:
        outline = await generate_course_outline(sample_course)
        print("\nGenerated Outline:\n")
        print(outline)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 