# Week4 - Particle Filter

본 과제는 particle filter의 update부분과 resampling 부분을 구현하는 것이다.



우선 update부분을 살표보도록 하겠다.

![image](https://user-images.githubusercontent.com/12128784/115054049-bf287d80-9f1a-11eb-9e38-84f8a4c64f40.png)




다음으로는 sampling을 하는 부분이다. sampling을 하는 부분은 numpy의 random.choice를 사용하면 쉽게 구할 수 있다.

![image](https://user-images.githubusercontent.com/12128784/114960351-ccedec80-9ea1-11eb-9e04-90aa4e0b1c51.png)
