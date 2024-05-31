import secrets
import os 

class Starbeautyvote : 
    def __init__(self) -> None:
        pass
    
    def generate_random_string(length=16):
        """
        Generates a random alphanumeric string of specified length.

        Args:
            length (int, optional): The desired length of the random string. Defaults to 10.

        Returns:
            str: A random alphanumeric string.
        """
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return ''.join(secrets.choice(chars) for _ in range(length))
    
    def modify_filename(filename,image_name):
	    # Change the filename from a.jpg to ab.jpg
        new_filename = image_name + os.path.splitext(filename)[1]
        return new_filename

    def voteNumberToFinalAmount(votes) : 
        votes = int(votes)
        numberOfTranches = votes // 10
        resteOfVote = votes % 10
        finalAmout = (numberOfTranches * 11 * 100) + (resteOfVote * 100)
        
        return finalAmout



