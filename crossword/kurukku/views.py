from django.shortcuts import render
from django.http import HttpResponse
from generator.matrix_generator import CrosswordGen

# Create your views here.

dd = [
{
    "answer": "ARJUN",
    "clue": "best archer of the pandavas"
},
{
    "answer": "KUNTHI",
    "clue": "mother of three of the pandavas"
},
{
    "answer": "GATOTHGAJAN",
    "clue": "son of bheema"
},
{
    "answer": "DWARAKA",
    "clue": "palace of krishna"
},
{
    "answer": "SHAKUNI",
    "clue": "master of dice game"
},

{
"answer": "KANCHIPURAM",
"clue": "purusheshu vishnu nagareshu ____"
},
{"answer": "THIRUVANNAMALAI",
"clue": "muthai thiru pathhi thirunagai"
},
{"answer": "THANJAVUR",
"clue": "Granary of south india"
},
{"answer": "MADURAI",
"clue": "kannagi hates this place"
},
{"answer": "KANYAKUMARI",
"clue": "vivekananda meditated here"
},
{"answer": "KUMBAKONAM",
"clue": "city of temples"
},
{"answer": "KAILASH",
"clue": "Heaven on earth"
},
{"answer": "THIRUKATTUPALLI",
"clue": "agneeshwarar kovil"
},
{"answer": "SAMAYAPURAM",
"clue": "mariamman"
},
{"answer": "NAMAKKAL",
"clue": "Growing hanuman lives here"
},
{"answer": "PALANI",
"clue": "famous avvaiyar incident took place here"
},
{"answer": "MAHABALIPURAM",
"clue": "sivakamiyin sabatham"
},
{"answer": "THIRUCHENDUR",
"clue": "Murugan killed surapadman and came here"
},
{"answer": "RAMESHWARAM",
"clue": "Sri Raman worshipped Shiva here"
},
{"answer": "TIRUPATHI",
"clue": "7 hills"
},
{"answer": "THIRUVARUR",
"clue": "Shri Thyagaraja was born here"
}
]

matrix_gen = CrosswordGen(lang='tamil')

def index(request):
    result = matrix_gen.generate_puzzle(words_clues=dd)

    context = {'puzzleData': result}
    return render(request, "base.html", context)
    # return HttpResponse("Hello, first page after a long time!!")

def new_puzzle_view(request):
    if request.method == 'POST':
        lang = request.POST.get('lang', "english")
        level = request.POST.get('level', '1')
        matrix_gen = CrosswordGen(lang=lang)
        result = matrix_gen.generate_puzzle(words_clues=dd)
        context = {'puzzleData': result}
        return render(request, "base.html", context)