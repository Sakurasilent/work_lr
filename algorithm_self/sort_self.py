class Solution(object):
    def bubble_sort(self, arr):
        """
        冒泡排序
        """
        arr_len = len(arr)
        for i in range(arr_len):
            swip = False
            for j in range(arr_len - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j+1] = arr[j+1],arr[j]
                    swip = True
            if not swip:
                    break
        return arr
    
    def selection_sort(self, arr):
        """
        选择排序
        """
        arr_len = len(arr)
        for i in range(arr_len):
            min_index = i
            for j in range(i + 1, arr_len):
                   if arr[j] < arr[i]:
                        min_index = j
            arr[min_index], arr[i] = arr[i], arr[min_index]
        return arr
    def insert_sort(self, arr):
        """
        插入排序
        """
        arr_len = len(arr)
        for i in range(1, arr_len):
            key = arr[i]
            j = i - 1

            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j+1] = key
        return arr

    def shell_sort(self, arr):
        """
        希尔排序
        todo 10
        """
        arr_len = len(arr)
        gap = arr_len // 2
        while gap>0:
            for i in range(gap, arr_len):
                key = arr[i]
                j = i
                while j >= gap and key < arr[j-gap]:
                    arr[j] = arr[j-gap]
                    j -= gap
                arr[j]=key
            gap//=2
        return arr
    
    def quick_sort(self, arr):
        """快速排序"""
        if len(arr)<=1:
            return arr
        pivot = arr[-1]
        pivot_left = [x for x in arr[:-1] if x < pivot]
        pivot_right = [x for x in arr[:-1] if x >= pivot]
        return self.quick_sort(pivot_left)+pivot+self.quick_sort(pivot_right)
    
    
    def __merge(self, left_arr, right_arr):
        l, r = 0, 0
        curr_sort_arr = []
        while l < len(left_arr) and r < len(right_arr):
            if left_arr[l] < right_arr[r]:
                curr_sort_arr.append(left_arr[l])
                l+=1
            else:
                curr_sort_arr.append(right_arr[r])
                r+=1
        curr_sort_arr.extend(left_arr[l:])
        curr_sort_arr.extend(right_arr[r:])
        return curr_sort_arr
    def merge_sort(self, arr):
        """
        归并排序
        """
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2

        left_mid = self.merge_sort(arr[:mid])
        right_mid = self.merge_sort(arr[mid:])

        return self.__merge(left_mid, right_mid)
        
    
if __name__ == "__main__":
    fl = Solution()
    arr_v1 = [2,4,1,6,5,3,8,9,1]
    print(arr_v1)
    # res = fl.bubble_sort(arr_v1)
    # res = fl.selection_sort(arr_v1)
    # res = fl.insert_sort(arr_v1)
    # res = fl.shell_sort(arr_v1)
    res = fl.merge_sort(arr_v1)
    print(res)
    pass