# W3M2b
#### 4개의 xml files들을 살펴 보고 각 화일의 셋팅 중에 중요하거나 유용하다고 생각되는 것들을 각자 골라서 용법을 파악해 보세요. 

1. core-site.xml : fs.defaultFS
    - 이유: hdfs의 핵심이 되는 namenode를 변경할 때 유용하게 사용될 수 있음. 변경한 url을 가진 namenode를 실행하고, 재시작하면 변경가능. 

2. core-site.xml : io.file.buffer.size
    - 이유: i/o에서 병목이 자주 발생하기 때문에 적절히 조절해야한다. 너무 작으면 속도가 느려지고, 너무 크게 설정되면 버퍼마다 빈 공간이 많이 발생한다. 

3. hdfs-site.xml : dfs.replication
    - 이유: datalocal과 racklocal 개념과 tradeoff되는 환경변수. 적절히 조절하여 비즈니스 목적과 현재 제한상황을 모두 달성할 수 있는 값을 설정해야함.

# W3M4
#### 'predefined keywords'가 아닌 다른 방법으로 나누고자 한다면 어떤 방법이 있을까요? 팀과 함께 논의해서 다른 방법을 시도해 보세요.

- **predefined keywords**: tweet에 대한 sentiment label
- 다른 방법으로 나누는 방법?
    - label을 다는 방법을 다르게 해라.
    - label이 없을 때, label을 다는 방법을 고민해라.
    - 만약, mapper에 sentiment를 분류하는 코드를 넣은다면?
        - 모델을 분산 컴퓨팅 환경에 적용하는 방법을 고민해야함.
            - 모델을 직접 설치?
            - API로 모델을 제공?
