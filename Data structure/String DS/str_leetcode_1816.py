class Solution:
    def truncateSentence(self, s: str, k: int) -> str:
        s_split = s.split()
        return " ".join(s_split[0:k])

sol = Solution()
print(sol.truncateSentence("Hi how are you doing what why",5)) 