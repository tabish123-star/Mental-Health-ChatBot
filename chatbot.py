import re
from typing import Dict, List


class MentalHealthChatbot:
    """
    Simple rule-based mental health support chatbot.

    This project is designed for learning FastAPI, Python,
    text processing, APIs, and basic conversational logic.
    It does NOT diagnose medical conditions.
    """

    def __init__(self):
        self.crisis_keywords = [
            "kill myself",
            "suicide",
            "suicidal",
            "end my life",
            "take my life",
            "hurt myself",
            "harm myself",
            "self harm",
            "self-harm",
            "want to die",
            "wish i was dead",
            "don't want to live",
            "do not want to live",
        ]

        self.intent_keywords = {
            "greeting": [
                "hello", "hi", "hey", "salam",
                "good morning", "good evening"
            ],
            "anxiety": [
                "anxious", "anxiety", "panic",
                "worried", "worry", "nervous",
                "overthinking", "fear"
            ],
            "stress": [
                "stress", "stressed", "pressure",
                "workload", "burnout", "overwhelmed"
            ],
            "sadness": [
                "sad", "unhappy", "crying",
                "lonely", "loneliness", "depressed",
                "down", "hopeless"
            ],
            "anger": [
                "angry", "anger", "mad",
                "frustrated", "frustration", "irritated"
            ],
            "sleep": [
                "sleep", "insomnia", "can't sleep",
                "cannot sleep", "awake", "tired"
            ],
            "motivation": [
                "motivation", "motivated",
                "lazy", "productive", "focus",
                "concentration"
            ],
            "thanks": [
                "thanks", "thank you", "thx",
                "appreciate it"
            ],
        }

        self.responses = {
            "greeting": [
                "Hello! I am here to listen. How are you feeling today?",
                "Hi! You can share what is on your mind. I will listen without judgment.",
            ],
            "anxiety": [
                "It sounds like you may be dealing with a lot of worry. Try taking a slow breath and focus on one thing you can control right now.",
                "When anxiety feels strong, try inhaling slowly for four seconds and exhaling for six seconds. You can also write down the thought that is worrying you.",
            ],
            "stress": [
                "It sounds like you are under pressure. Consider breaking your responsibilities into smaller tasks and taking a short break between them.",
                "Stress can feel overwhelming. Try identifying the one task that matters most right now instead of trying to solve everything at once.",
            ],
            "sadness": [
                "I am sorry you are having a difficult time. Talking to someone you trust or doing one small comforting activity may help you feel less alone.",
                "It is okay to acknowledge difficult feelings. You do not have to solve everything immediately. What has been weighing on you the most?",
            ],
            "anger": [
                "It sounds like something has really frustrated you. Before responding, consider taking a short pause and a few slow breaths.",
                "Strong anger can make situations feel more intense. Giving yourself some space before making a decision can help.",
            ],
            "sleep": [
                "For better sleep, try keeping a consistent bedtime, reducing screen use before bed, and creating a calm environment.",
                "If sleep problems continue or seriously affect your daily life, consider discussing them with a qualified healthcare professional.",
            ],
            "motivation": [
                "Try starting with a task that takes only five minutes. Small progress can make the next step feel easier.",
                "You do not need to finish everything at once. Pick one realistic goal and work on it for a short period.",
            ],
            "thanks": [
                "You're welcome. I am glad I could listen.",
                "You're welcome. Take care of yourself.",
            ],
            "default": [
                "I hear you. Can you tell me a little more about what you are experiencing?",
                "Thank you for sharing that. What part of this situation feels hardest for you right now?",
                "That sounds important. Would you like to describe what happened and how it made you feel?",
            ],
        }

    def clean_text(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"\s+", " ", text)
        return text

    def detect_crisis(self, text: str) -> bool:
        cleaned = self.clean_text(text)
        return any(keyword in cleaned for keyword in self.crisis_keywords)

    def detect_intent(self, text: str) -> str:
        cleaned = self.clean_text(text)

        scores = {}
        for intent, keywords in self.intent_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in cleaned:
                    score += 1
            scores[intent] = score

        best_intent = max(scores, key=scores.get)

        if scores[best_intent] == 0:
            return "default"

        return best_intent

    def detect_mood(self, text: str) -> str:
        cleaned = self.clean_text(text)

        mood_words = {
            "happy": [
                "happy", "great", "good",
                "excited", "wonderful", "joy"
            ],
            "sad": [
                "sad", "unhappy", "crying",
                "lonely", "hopeless"
            ],
            "anxious": [
                "anxious", "anxiety",
                "worried", "panic", "nervous"
            ],
            "angry": [
                "angry", "mad", "frustrated",
                "irritated"
            ],
            "stressed": [
                "stress", "stressed",
                "pressure", "overwhelmed"
            ],
            "tired": [
                "tired", "exhausted",
                "sleepy", "fatigued"
            ],
            "calm": [
                "calm", "relaxed",
                "peaceful", "okay", "fine"
            ],
        }

        scores = {}
        for mood, words in mood_words.items():
            scores[mood] = sum(word in cleaned for word in words)

        best_mood = max(scores, key=scores.get)

        if scores[best_mood] == 0:
            return "neutral"

        return best_mood

    def crisis_response(self) -> str:
        return (
            "I am really sorry you are going through this. "
            "If you may hurt yourself or someone else, please move "
            "away from anything you could use to cause harm and stay "
            "with a trusted person. Contact your local emergency service "
            "or a crisis service in your country now. If possible, tell "
            "someone you trust exactly what you are experiencing. "
            "I can continue listening, but I cannot provide emergency care."
        )

    def get_response_for_intent(self, intent: str) -> str:
        options = self.responses.get(
            intent,
            self.responses["default"]
        )

        # Deterministic choice keeps the demo easy to test.
        return options[0]

    def generate_response(self, message: str) -> Dict:
        if not message or not message.strip():
            return {
                "response": "Please tell me what is on your mind.",
                "mood": "neutral",
                "crisis_detected": False,
                "intent": "default",
            }

        crisis = self.detect_crisis(message)
        mood = self.detect_mood(message)

        if crisis:
            return {
                "response": self.crisis_response(),
                "mood": mood,
                "crisis_detected": True,
                "intent": "crisis",
            }

        intent = self.detect_intent(message)
        response = self.get_response_for_intent(intent)

        return {
            "response": response,
            "mood": mood,
            "crisis_detected": False,
            "intent": intent,
        }


def demo():
    bot = MentalHealthChatbot()

    examples: List[str] = [
        "Hello",
        "I feel very anxious about my exams.",
        "I am stressed because I have too much work.",
        "I feel lonely today.",
        "I cannot sleep properly.",
    ]

    for message in examples:
        result = bot.generate_response(message)
        print("=" * 50)
        print("User:", message)
        print("Mood:", result["mood"])
        print("Intent:", result["intent"])
        print("Bot:", result["response"])


if __name__ == "__main__":
    demo()
