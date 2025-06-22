import pickle

data = {'messages': 'Hello'}

with open('test_input.pkl', 'wb') as f:
    pickle.dump(data, f)