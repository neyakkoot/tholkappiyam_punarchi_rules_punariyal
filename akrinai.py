import tamil

def akrinai(பெயர்):
  அஃறிணை_ஒன்றன்பால்_ஈறு = ['து', 'று', 'டு']
  அஃறிணை_பலவின்பால்_ஈறு = ['அ', 'ஆ', 'வ']

  அஃறிணை_ஈறு = ['து', 'று', 'டு','அ', 'ஆ', 'வ']

  பெயர்_பிரி2 = tamil.utf8.get_letters(பெயர்)
  அஃறி_இறுதி_எழுத்து = பெயர்_பிரி2[-1]

  if அஃறி_இறுதி_எழுத்து in அஃறிணை_ஈறு:
    return ('ஆம். இது அஃறிணைச் சொல்தான்')
  
  else:
    return ('இல்லை. இது அஃறிணைச் சொல் இல்லை. வேறு ஒரு சொல்லினைத் தந்து ஆய்வு செய்க.')
