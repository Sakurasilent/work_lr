class Solution(object):
    """
    https://leetcode.cn/problems/4sum/description/?envType=problem-list-v2&envId=sorting
    """
    def fourSum(self, nums, target):
        
        result=[]
        # 排序
        nums.sort()
        for i in range(len(nums)-1):
            for j in range(i+1,len(nums)):
                if j > i + 1 and nums[j] == nums[j-1]:
                    continue
                k = j + 1
                l = len(nums)-1
                while k < l:
                    if k > j + 1 and nums[k]==nums[k - 1]and k+1<l:
                        k += 1
                    if l < len(nums) - 1 and nums[l] == nums[l + 1] and l-1 > k:
                        l -= 1
                    curr_target = nums[i] + nums[j] + nums[k] + nums[l]
                    if  curr_target == target:
                        print([nums[i], nums[j], nums[k], nums[l]])
                        if [nums[i], nums[j], nums[k], nums[l]] not in result:
                            result.append([nums[i], nums[j], nums[k], nums[l]])
                        l -= 1
                        k += 1
                    if curr_target > target:
                        l -= 1
                    elif curr_target<target:
                        k += 1
        return result


if __name__ == "__main__":
    fl = Solution()
    nums =  [-2,-1,-1,1,1,2,2]
    print(nums)
    target = 0
    res = fl.fourSum(nums=nums,target=target)
    print(res)
    