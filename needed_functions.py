#txt = "Bangladesh is our favourite country? I love you. Because of love you, I can not but sleep. love is the best."

def question_mark_traker(data:dict):
    #Trcking the tracking question mark.
    striping_text = data['msg'].split()
    for i,word in enumerate(striping_text):
        if data['dep'] == True:
            if i >= 2 and word.count("?") :
                print(word)
                print(i)
                print("Passed...")
                return True
        elif word.count(".") != 0:
            if i >= 2:
                print(word)
                print("Passed...")
                return True
            


