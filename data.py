from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

languages = {'Afrikaans': 'af', 'Arabic': 'ar', 'Bulgarian': 'bg', 'Bengali': 'bn',
                   'Bosnian': 'bs', 'Catalan': 'ca', 'Czech': 'cs', 'Danish': 'da',
                   'German': 'de', 'Greek': 'el', 'English': 'en', 'Spanish': 'es',
                   'Estonian': 'et', 'Finnish': 'fi', 'French': 'fr', 'Gujarati': 'gu',
                   'Hindi': 'hi', 'Croatian': 'hr', 'Hungarian': 'hu', 'Indonesian': 'id',
                   'Icelandic': 'is', 'Italian': 'it', 'Hebrew': 'iw', 'Japanese': 'ja',
                   'Javanese': 'jw', 'Khmer': 'km', 'Kannada': 'kn', 'Korean': 'ko',
                   'Latin': 'la', 'Latvian': 'lv', 'Malayalam': 'ml', 'Marathi': 'mr',
                   'Malay': 'ms', 'Myanmar (Burmese)': 'my', 'Nepali': 'ne', 'Dutch': 'nl',
                   'Norwegian': 'no', 'Polish': 'pl', 'Portuguese': 'pt', 'Romanian': 'ro',
                   'Sinhala': 'si', 'Slovak': 'sk', 'Albanian': 'sq',
                   'Serbian': 'sr', 'Sundanese': 'su', 'Swedish': 'sv', 'Swahili': 'sw',
                   'Tamil': 'ta', 'Telugu': 'te', 'Thai': 'th', 'Filipino': 'tl',
                   'Turkish': 'tr', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Vietnamese': 'vi',
                   'Chinese (Simplified)': 'zh-CN',
                   'Chinese (Mandarin/Taiwan)': 'zh-TW', 'Chinese (Mandarin)': 'zh'}


def get_params():
    estimates = np.array([[37, 18], [172, 68], [1224, 577], [154, 197],
                          [1551, 682], [37, 37], [37, 39], [37, 20], [6910, 6263],
                          [16066, 13819], [5162, 3849], [7961, 6902], [6910, 5861],
                          ])

    lr = LinearRegression()
    x = np.sqrt(estimates[:, 0].reshape(-1, 1))
    scaler = StandardScaler()
    x_norm = scaler.fit_transform(x)
    y = estimates[:, 1].reshape(-1, )
    lr.fit(x_norm, y)
    b = lr.intercept_
    w = lr.coef_[0]
    return w, b


param1, param2 = get_params()
print(param1, param2)
param1 = 0.45184007
param2 = -0.4095843748955872

