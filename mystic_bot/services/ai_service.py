from openai import OpenAI
from config import AI_API_KEY, AI_API_BASE_URL, AI_MODEL

class AIService:
    def __init__(self):
        self.client = OpenAI(
            api_key=AI_API_KEY,
            base_url=AI_API_BASE_URL
        )
        self.model = AI_MODEL
    
    def get_tarot_reading(self, question: str, spread_type: str = "single") -> str:
        """Получить расклад Таро"""
        system_prompt = """Ты опытный таролог с многолетней практикой. 
        Ты даешь глубокие, мудрые и полезные интерпретации карт Таро.
        Твой стиль - теплый, поддерживающий, но честный.
        Избегай фатализма, вместо этого давай практические советы."""
        
        user_prompt = f"""Вопрос пользователя: {question}
        Тип расклада: {spread_type}
        
        Проведи расклад Таро и дай подробную интерпретацию."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
    
    def get_astrology_reading(self, birth_date: str, birth_time: str, birth_place: str, question: str) -> str:
        """Получить астрологическую консультацию"""
        system_prompt = """Ты профессиональный астролог.
        Ты анализируешь натальные карты, транзиты и прогрессии.
        Даешь точные и полезные астрологические прогнозы.
        Объясняешь сложные аспекты простым языком."""
        
        user_prompt = f"""Дата рождения: {birth_date}
        Время рождения: {birth_time}
        Место рождения: {birth_place}
        Вопрос: {question}
        
        Дай астрологический анализ и ответ на вопрос."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
    
    def get_rune_reading(self, question: str, spread_type: str = "three_runes") -> str:
        """Получить рунический расклад"""
        system_prompt = """Ты опытный рунолог, знаток северной традиции.
        Ты работаешь со Старшим Футарком.
        Даешь глубокие интерпретации рун, учитывая их положение и взаимосвязи.
        Твой стиль - мудрый, образный, с отсылками к скандинавской мифологии."""
        
        user_prompt = f"""Вопрос пользователя: {question}
        Тип расклада: {spread_type}
        
        Проведи рунический расклад и дай подробную интерпретацию."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
    
    def get_general_consultation(self, message: str) -> str:
        """Общая консультация по любым эзотерическим вопросам"""
        system_prompt = """Ты универсальный эзотерический консультант: таролог, астролог и рунолог.
        Ты обладаешь глубокими знаниями во всех этих областях.
        Отвечаешь мудро, поддерживающе, давая практические рекомендации.
        Если вопрос требует специфического инструмента (Таро, астрология, руны), предложи это пользователю."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
