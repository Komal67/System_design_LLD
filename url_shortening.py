import string

class Base62Encoder:
    def __init__(self):
        self.characters = string.ascii_letters+string.digits
        self.base=len(self.characters)

# Function to encode a number to Base62
    def encode(self,number):
        print(number)
        if number == 0:
            return self.characters[0]
        
        result =[]
        while number >0:
            print(self.base,number%self.base)
            result.append(self.characters[number%self.base])
            number = number//self.base
        
        return ''.join(reversed(result))

# Function to decode a Base62 string to a number
    def decode(self,short_url):
        number=0
        for char in short_url:
            number = number*self.base+self.characters.index(char)
        return number


class UrlShortner:
    def __init__(self):
        self.url_to_id={}
        self.id_to_url={}
        self.id_counter=0
        self.base62=Base62Encoder()
    
    def shorten_url(self,long_url):

        if long_url in self.url_to_id:
            url_id=self.url_to_id[long_url]
        else:
            self.id_counter+=1
            url_id=self.id_counter
            self.url_to_id[long_url]=url_id
            self.id_to_url[url_id]=long_url
        
        short_url=self.base62.encode(url_id)
        return short_url

    

    def expand_url(self,short_url):
        url_id=self.base62.decode(short_url)

        return self.id_to_url.get(url_id,"URL not found")


url_shortner=UrlShortner()

# Shortening a URL
long_url = "https://www.example.com/some/really/long/url"
short_url = url_shortner.shorten_url(long_url)
print(f"Shortened URL: {short_url}")
print(url_shortner.url_to_id)


# Expanding the shortened URL
original_url = url_shortner.expand_url(short_url)
print(f"Original URL: {original_url}")