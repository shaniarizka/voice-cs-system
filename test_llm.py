from app.llm import generate_response

text = "Aku mau book flight ke Jeddah minggu depan"

print("\n=== MODE PRESERVE ===")
result1 = generate_response(text, mode="preserve")
print(result1)

print("\n=== MODE NORMALIZE ===")
result2 = generate_response(text, mode="normalize")
print(result2)