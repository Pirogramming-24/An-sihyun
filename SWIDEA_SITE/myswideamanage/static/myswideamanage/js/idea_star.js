/**
 * 1. 공용 함수: 장고 보안을 위한 CSRF 토큰 가져오기
 * 이 함수가 맨 위에 있어야 아래 모든 함수에서 자유롭게 사용할 수 있습니다.
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * 2. 별 찜하기 기능 (Toggle Star)
 */
function toggleStar(ideaId, element) {
    const csrftoken = getCookie('csrftoken');

    fetch("/star_toggle/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({ id: ideaId })
    })
    .then(response => response.json())
    .then(data => {
        // [핵심] 여기서 색상을 명확하게 지정해버립니다.
        if (data.is_starred) {
            // 찜 상태면 무조건 노란색
            element.style.color = "#f2f26aff"; 
        } else {
            // 찜 해제면 무조건 연한 회색 (처음 그 색상)
            element.style.color = "#ccc"; 
        }
    })
    .catch(error => console.error('Error:', error));
}

/**
 * 3. 관심도 조절 기능 (+/- 버튼)
 */
function updateInterest(ideaId, action) {
    const csrftoken = getCookie('csrftoken');

    fetch("/interest_update/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({ 
            id: ideaId, 
            action: action 
        })
    })
    .then(response => {
        if (!response.ok) throw new Error('네트워크 응답 에러');
        return response.json();
    })
    .then(data => {
        // 서버가 계산해서 보내준 새로운 관심도 숫자를 화면에 반영
        // HTML에 id="interest-count-{{ idea.id }}"가 있어야 합니다.
        const countElement = document.getElementById(`interest-count-${ideaId}`);
        if (countElement) {
            countElement.innerText = data.interest;
        }
    })
    .catch(error => console.error('Error:', error));
}