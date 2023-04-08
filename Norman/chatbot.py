from chatterbot import ChatBot
from chatterbot.comparisons import LevenshteinDistance,SentimentComparison,SynsetDistance
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_most_frequent_response


bot = ChatBot(
    'Betaways',read_only=True,
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    filters = [
        'chatterbot.filters.get_recent_repeated_responses'
    ],
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function":LevenshteinDistance,
            "response_selection_method":get_most_frequent_response
        }
    ],
    database_uri='sqlite:///database.sqlite3',
)

trainer = ChatterBotCorpusTrainer(bot)
trainer.train(
    "chatterbot.corpus.english",
    "Norman/corpus_data/salamu.yml",
    "Norman/corpus_data/stopwords.yml",
    "Norman/corpus_data/chakula.yml",
    "Norman/corpus_data/mazungumzo.yml",
    

)
while True:
    try:
        bot_input = bot.get_response(input())
        print(bot_input)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break