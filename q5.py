# Python3 program to find maximum possible AND

# Function to check whether a k segment partition
# is possible such that bitwise AND is 'mask'
def checkpossible(mask, arr, prefix, n, k):
    # dp[i][j] stores whether it is possible to partition
    # first i elements into j segments such that all j
    # segments are 'good'
    dp = [[0 for i in range(k + 1)] for i in range(n + 1)]

    # Initialising dp
    dp[0][0] = 1

    # Filling dp in bottom-up manner
    for i in range(1, n + 1):
        for j in range(1, k + 1):

            # Finding a cut such that first l elements
            # can be partitioned into j-1 'good' segments
            # and arr[l+1]+...+arr[i] is a 'good' segment
            for l in range(i - 1, -1, -1):
                if (dp[l][j - 1] and (((prefix[i] - prefix[l]) & mask) == mask)):
                    dp[i][j] = 1
                    break

    return dp[n][k]


# Function to find maximum possible AND
def Partition(arr, n, k):
    # Array to store prfix sums
    prefix = [0 for i in range(n + 1)]

    for i in range(1, n + 1):
        prefix[i] = prefix[i - 1] + arr[i]

    # Maximum no of bits in the possible answer
    LOGS = 20

    # This will store the final answer
    ans = 0

    # Constructing answer greedily selecting
    # from the higher most bit
    for i in range(LOGS, -1, -1):
        # Checking if array can be partitioned
        # such that the bitwise AND is ans|(1<<i)
        if (checkpossible(ans | (1 << i), arr, prefix, n, k)):
            # if possible, update the answer
            ans = ans | (1 << i)

    # Return the final answer
    return ans


# Driver code

arr = [9, 14, 28, 1, 7, 13, 15, 29, 2, 31]
k = 4

# n = 11 , first element is zero
# to make array 1 based indexing. So, number of
# elements are 10
n = len(arr) - 1

# Function call
print(Partition(arr, n, k))

# This code is contributed by mohit kumar 29
