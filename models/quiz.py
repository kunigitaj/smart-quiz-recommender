# models/quiz.py

from typing import List, Dict

class QuizOption:
    def __init__(self, id: str, text: str, translations: Dict[str, str]):
        self.id = id
        self.text = text
        self.translations = translations

class AnswerExplanation:
    def __init__(self, text: str, translations: Dict[str, str]):
        self.text = text
        self.translations = translations

class ReflectionPrompt:
    def __init__(self, text: str, translations: Dict[str, str]):
        self.text = text
        self.translations = translations

class Hint:
    def __init__(self, text: str, translations: Dict[str, str]):
        self.text = text
        self.translations = translations

class AdaptiveDifficulty:
    def __init__(self, cognitive_load: str, engagement_level: str, prior_knowledge: str, confidence_level: str):
        self.cognitive_load = cognitive_load
        self.engagement_level = engagement_level
        self.prior_knowledge = prior_knowledge
        self.confidence_level = confidence_level

class QuizQuestion:
    def __init__(self, title: str, title_translations: Dict[str, str], options: List[QuizOption], correct_option: str, tags: List[str], difficulty: str, learning_objectives: List[str], answer_explanation: AnswerExplanation, reflection_prompt: ReflectionPrompt, hint: Hint, estimated_time: int, adaptive_difficulty: AdaptiveDifficulty, topic: str, subtopic: str):
        self.title = title
        self.title_translations = title_translations
        self.options = options
        self.correct_option = correct_option
        self.tags = tags
        self.difficulty = difficulty
        self.learning_objectives = learning_objectives
        self.answer_explanation = answer_explanation
        self.reflection_prompt = reflection_prompt
        self.hint = hint
        self.estimated_time = estimated_time
        self.adaptive_difficulty = adaptive_difficulty
        self.topic = topic
        self.subtopic = subtopic

class Quiz:
    def __init__(self, quiz_id: str, section_id: str, title: str, category: str, description: str, thumbnail: str, tags: List[str], questions: List[QuizQuestion]):
        self.quiz_id = quiz_id
        self.section_id = section_id
        self.title = title
        self.category = category
        self.description = description
        self.thumbnail = thumbnail
        self.tags = tags
        self.questions = questions
