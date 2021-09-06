# HTML에 수학 수식 넣기

HTML은 기본적으로 수학 수식을 지원하지 않는다.

특수 기호를 사용하여 어느 정도 흉내는 낼 수 있지만, 아주 귀찮은 수작업이다.

그렇기 때문에, __MathJax__ 라는 수학 수식 자동변환 javascript 라이브러리를 사용한다.

## MathJax?

MathJax는 지정된 방식으로 작성된 HTML 코드를 수학 수식으로 변환해주는 javascript 라이브러리 이다.

홈페이지 링크 : [https://www.mathjax.org/](https://www.mathjax.org/)

예를 들어, 일차방정식 __ax = b__ 을 HTML에 반영한다고 보면 코드는 `\(ax = b\)` 로 되고 결과는 밑에와 같이 나온다.

![mathequation](https://user-images.githubusercontent.com/44990492/132163856-d6f48536-050f-49b3-9d3e-6903493f88da.PNG)

## 사용방법

사용방법은 엄청 간단하다. 라이브러리를 호출하고, HTML 코드 내에 아무대나 수학 수식 코드 넣어주면, 페이지 로드 시 자동으로 수학 수식을 변환해준다.

일단은 MathJax 라이브러리를 호출해야 한다.

```html
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async
        src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
</script>
```

### inline 수식

inline 수식은 `\( .. \)`과 같은 방법으로 작성이 가능하다.

코드:

```html
<p>
  Given vectors \(u\), \(v\) and \(w\),
</p>
```

결과:

![mathequation_3](https://user-images.githubusercontent.com/44990492/132163861-73708b8b-510c-40b0-af86-dd4ba165d469.PNG)

### block 수식

block 수식은 `\[ .. \]`과 같은 방법으로 가능하다.

코드:

```html
<p>
  Given vectors \(u\), \(v\) and \(w\),
  we can form the linear combination \[x_{1}u + x_{2}v + x_{3}w = b\].
</p>
```

결과:

![mathequation_4](https://user-images.githubusercontent.com/44990492/132163862-a36224df-0fde-488e-84df-25c6b201db91.PNG)

### complex 수식

일차연릭방정식 같이 좀 더 복잡한 수식은 밑에와 같다.

코드:

```tex
$$
\left\{ 
\begin{array}{c}
a_1x+b_1y+c_1z=d_1 \\ 
a_2x+b_2y+c_2z=d_2 \\ 
a_3x+b_3y+c_3z=d_3
\end{array}
\right. 
$$
```

결과:

![mathequation_2](https://user-images.githubusercontent.com/44990492/132163860-54c0de04-a27f-4a3b-81e7-56b09c149c7b.PNG)

해당 가이드는 모든 사용방법을 카바하지 않는다.
그냥 이런게 있다~ 라는 정도만 이해하면 된다.

## References

1. 공식 홈페이지 가이드 [(링크)](http://docs.mathjax.org/en/latest/)
2. LaTex 치트시트 [(링크)](http://tug.ctan.org/info/undergradmath/undergradmath.pdf)
   - __pandoc__을 사용해서 LaTex를 MathJax로 변환할 수 있다. [온라인 변환기](https://pandoc.org/try/), [예시](https://pandoc.org/demos.html#)
3. 저자가 찾은 최고 가이드 [(링크)](https://math.meta.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference)

