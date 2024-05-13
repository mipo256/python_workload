from typing import List

from math import pow

class Solution:

    def __init__(self, reward_array, time_probability_matrix) -> None:
        self.reward_array = reward_array
        self.time_probability_matrix = time_probability_matrix
        self.target = self.requireTarget()        
        self.time_range = self.requireTimeRange()

    def prepare_bin(self, b) -> int:
        return b[2:]
    
    def toIntSafe(self, arg: any) -> int:
        try:
            return int(arg)
        except TypeError:
            print(f"Перданное значение '{arg}' не является integer-ом")
            exit(1)

    def requireInt(self, text: str, default: int) -> int:
        target = input(text)
        
        if target is None or len(target.strip()) == 0:
            return default
        
        return self.toIntSafe(target)

    def requireTarget(self) -> int:
        default = 12
        return self.requireInt(f"Введите пороговый балл ({default} по умолчанию): ", default)
    
    def requireTimeRange(self) -> List[int]:
        left_default = 1640
        right_deafult = 3790
        return [
            self.requireInt(f"Введите нижнею границу временного диапазона ({left_default} по умолчанию): ", left_default),
            self.requireInt(f"Введите верхнею границу временного диапазона ({right_deafult} по умолчанию): ", right_deafult) 
        ]

    def checkTarget(self, binary: bin, target: int) -> bool:        
        sum = 0

        for i in range(len(binary) - 1, -1, -1):
            if binary[i] == '1':
                task_index = len(self.reward_array) - (len(binary) - i)
                sum += self.reward_array[task_index]
        
        return sum >= target
    
    def zero_extend(self, s):
        while len(s) != 10:
            s = "0" + s
        else:
            return s

    def printResult(self, binary, probability, totalTime) -> None:
        print(f"""
        Удоавлетворяющий сценарий: {self.zero_extend(binary)},
        Суммарное время: {totalTime},
        Вероятность события: {probability}
        ----------------------------------------
        """)

    def deepCheck(self, binary, i, accumulatedTime: int, accumulatedProbability : float) -> None:
        """
        visitedMap example:
        {
            9 -> [0, 0, 0]
            8 -> [1, 1, 0]
            7 -> [1, 1, 1]
        }
        """
        while i >= 0 and binary[i] != '1':
            i -= 1

        if i < 0:
            if (self.time_range[0] <= accumulatedTime and self.time_range[1] >= accumulatedTime):
                self.printResult(binary, accumulatedProbability, accumulatedTime)
            return

        task_index = len(self.reward_array) - (len(binary) - i)
        current_time_rpbability_matrix : dict = self.time_probability_matrix[task_index]

        for time, probability in current_time_rpbability_matrix.items():
            self.deepCheck(binary, i - 1, accumulatedTime + time, probability * accumulatedProbability)

    def main(self):
        for n in range(0, int(pow(2, 10))):
            binary = self.prepare_bin(str(bin(n)))
            if self.checkTarget(binary, self.target):
                self.deepCheck(binary, len(binary) - 1, 0, 1.0)

if __name__ == "__main__":
    Solution(
        [1, 1, 1, 1, 1, 2, 3, 2, 4, 3],
        [
            {
                60: 0.3,
                180: 0.5,
                300: 0.2
            },
            {
                75: 0.15,
                190: 0.6,
                330: 0.25
            },
            {
                60: 0.15,
                120: 0.35,
                250: 0.5
            },
            {
                130: 0.1,
                200: 0.3,
                350: 0.6
            },
            {
                75: 0.2,
                140: 0.45,
                210: 0.35
            },
            {
                200: 0.2,
                275: 0.35,
                380: 0.45
            },
            {
                310: 0.2,
                380: 0.4,
                450: 0.4
            },
            {
                200: 0.25,
                290: 0.4,
                370: 0.35
            },
            {
                380: 0.1,
                470: 0.25,
                650: 0.65
            },
            {
                150: 0.3,
                275: 0.55,
                500: 0.15
            }
        ]
    ).main()
