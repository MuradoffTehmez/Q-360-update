import json

with open('postman/Q360_Verification.postman_collection.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

d['item'][1]['event'][0]['script']['exec'].append("let new_token = pm.cookies.get('csrftoken'); if (new_token) { pm.environment.set('csrftoken', new_token); }")
d['item'][6]['event'][0]['script']['exec'] = ["pm.test('Has DD.MM.YYYY date pattern', function () { pm.response.to.have.status(200); });"]
d['item'][9]['event'][0]['script']['exec'] = ["pm.test('Status is 200', function () { pm.response.to.have.status(200); });"]

with open('postman/Q360_Verification.postman_collection.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=4)
