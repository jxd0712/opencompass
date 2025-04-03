LANG_TO_INSTRUCTIONS1 = {
    'en': 'What does the person mean by the proverb?',
    'bn': 'ব্যক্তি প্রবাদ দ্বারা কি বোঝায়?',
    'de': 'Was meint die Person mit dem Sprichwort?',
    'id': 'Apa yang dimaksud oleh orang tersebut dengan peribahasa itu?',
    'ru': 'Что человек подразумевает под этой пословицей?',
    'zh': '这个人说这句谚语是什么意思？'
}
LANG_TO_INSTRUCTIONS2 = {
    'en': 'Please choose between A and B.',
    'bn': 'দয়া করে A এবং B এর মধ্যে নির্বাচন করুন।',
    'de': 'Bitte wählen Sie zwischen A und B.',
    'id': 'Silakan pilih antara A dan B.',
    'ru': 'Пожалуйста, выберите между A и B.',
    'zh': '请在 A 和 B 之间做出选择。'
}
LANG_TO_INSTRUCTIONS3 = {
    'en': 'Please answer in one sentence in English.',
    'bn': 'বাংলায় এক বাক্যে উত্তর দিন।',
    'de': 'Bitte antworten Sie in einem Satz auf Deutsch.',
    'id': 'Tolong dijawab dalam satu kalimat dalam bahasa Indonesia.',
    'ru': 'Пожалуйста, ответьте одним предложением на русском языке.',
    'zh': '请用一句中文做出回答。'
}
LANG_TO_INSTRUCTIONS4 = {
    'en': 'Given a proverb and a conversation in which the proverb is used, explain what the person who said the proverb really meant based on the context of the conversation. Please do not just explain the meaning of the proverb itself, but describe the true intention of the person who said the proverb based on the context.',
    'bn': 'একটি প্রবাদ এবং একটি কথোপকথন দেওয়া হয়েছে যেখানে প্রবাদটি ব্যবহার করা হয়েছে, কথোপকথনের প্রেক্ষাপটের উপর ভিত্তি করে যে ব্যক্তি প্রবাদটি বলেছেন তিনি আসলে কী বোঝাতে চেয়েছিলেন তা ব্যাখ্যা করুন। অনুগ্রহ করে শুধু প্রবাদটির অর্থ ব্যাখ্যা করবেন না, তবে প্রসঙ্গটির উপর ভিত্তি করে যে ব্যক্তি প্রবাদটি বলেছেন তার প্রকৃত উদ্দেশ্য বর্ণনা করুন।',
    'de': 'Erklären Sie anhand eines Sprichworts und eines Gesprächs, in dem das Sprichwort verwendet wird, was die Person, die das Sprichwort verwendet hat, im Kontext des Gesprächs wirklich gemeint hat. Erklären Sie bitte nicht nur die Bedeutung des Sprichworts selbst, sondern beschreiben Sie die wahre Absicht der Person, die das Sprichwort verwendet hat, im Kontext.',
    'id': 'Jika diberi sebuah peribahasa dan percakapan yang menggunakan peribahasa tersebut, jelaskan apa yang sebenarnya dimaksudkan oleh orang yang mengucapkan peribahasa tersebut berdasarkan konteks percakapan. Jangan hanya menjelaskan arti dari peribahasa itu sendiri, tetapi jelaskan maksud sebenarnya dari orang yang mengucapkan peribahasa tersebut berdasarkan konteksnya.',
    'ru': 'Учитывая пословицу и разговор, в котором она используется, объясните, что на самом деле имел в виду человек, сказавший пословицу, основываясь на контексте разговора. Пожалуйста, не просто объясните значение самой пословицы, но и опишите истинное намерение человека, сказавшего пословицу, основываясь на контексте.',
    'zh': '给定一句谚语和一段使用了该谚语的对话，请根据对话语境，解释一下说出这句谚语的人真正想要表达的意思。请不要只解释谚语本身的含义，请结合语境来描述说出这句谚语的人的真正意图。'
}
judge_prompt_template = {
    'zh':
    '给定一段对话和关于该对话中人物意图的两句分析，请你判断这两句分析所表达的意思是否一致。\n\n对话：{conversation}\n分析1：{answer}\n分析2：{raw_pred}\n\n你只能回答YES或NO或UNSURE，请不要输出任何其它内容。你的回答：',  # noqa
    'en':
    "Given a conversation and two analyses of the characters' intentions in the conversation, please judge whether the two analyses express the same meaning. \n\nConversation: {conversation}\nAnalysis 1: {answer}\nAnalysis 2: {raw_pred}\n\nYou can only answer YES, NO or UNSURE, please do not output anything else. Your answer:",  # noqa
    'bn':
    'একটি কথোপকথন এবং কথোপকথনে চরিত্রগুলির উদ্দেশ্যগুলির দুটি বিশ্লেষণ দেওয়া, দুটি বিশ্লেষণ একই অর্থ প্রকাশ করে কিনা দয়া করে বিচার করুন৷ \n\nকথোপকথন: {conversation}\nবিশ্লেষণ 1: {answer}\nবিশ্লেষণ 2: {raw_pred}\n\nআপনি শুধুমাত্র YES, NO বা UNSURE উত্তর দিতে পারেন, অনুগ্রহ করে অন্য কিছু আউটপুট করবেন না। আপনার উত্তর:',  # noqa
    'de':
    'Gegeben sei ein Gespräch und zwei Analysen der Absichten der Charaktere im Gespräch. Beurteilen Sie bitte, ob die beiden Analysen dieselbe Bedeutung ausdrücken. \n\nGespräch: {conversation}\nAnalyse 1: {answer}\nAnalyse 2: {raw_pred}\n\nSie können nur YES, NO oder UNSURE beantworten, geben Sie bitte nichts anderes aus. Ihre Antwort:',  # noqa
    'id':
    'Diberikan sebuah percakapan dan dua analisis tentang maksud karakter dalam percakapan tersebut, mohon tentukan apakah kedua analisis tersebut mengungkapkan makna yang sama. \n\nPercakapan: {conversation}\nAnalisis 1: {answer}\nAnalisis 2: {raw_pred}\n\nAnda hanya dapat menjawab YES, NO atau UNSURE, mohon jangan berikan jawaban lain. Jawaban Anda:',  # noqa
    'ru':
    'Учитывая разговор и два анализа намерений персонажей в разговоре, пожалуйста, оцените, выражают ли два анализа одно и то же значение. \n\nРазговор: {conversation}\nАнализ 1: {answer}\nАнализ 2: {raw_pred}\n\nВы можете ответить только YES, NO или UNSURE, пожалуйста, не выводите ничего другого. Ваш ответ:'  # noqa
}
LANG_TO_PROVERBS = {
    'en': 'Proverb',
    'bn': 'প্রবাদ',
    'de': 'Sprichwort',
    'id': 'Pepatah',
    'ru': 'Пословица',
    'zh': '谚语'
}
LANG_TO_CONTEXTS = {
    'en': 'Context',
    'bn': 'প্রসঙ্গ',
    'de': 'Kontext',
    'id': 'konteks',
    'ru': 'Контекст',
    'zh': '背景'
}
LANG_TO_CHOICES = {
    'en': 'Choices',
    'bn': 'বিকল্পগুলি"',
    'de': 'Wahlmöglichkeiten',
    'id': 'Pilihan',
    'ru': 'Выборы',
    'zh': '选择'
}
LANG_TO_ANSWERS = {
    'en': 'Answer',
    'bn': 'উত্তর',
    'de': 'Antwort',
    'id': 'Jawaban',
    'ru': 'Ответить',
    'zh': '回答'
}
LANG_TO_QUESTIONS = {
    'en': 'Question',
    'bn': 'প্রশ্ন',
    'de': 'Frage',
    'id': 'Pertanyaan',
    'ru': 'Вопрос',
    'zh': '问题'
}
