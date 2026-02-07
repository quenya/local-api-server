import okhttp3.*;
import org.json.JSONObject;
import org.json.JSONArray;

import java.io.IOException;

/**
 * Java에서 로컬 API 서버 호출 예제
 * 
 * 필수 라이브러리:
 * - okhttp3:okhttp:4.11.0
 * - org.json:json:20231013
 */
public class LocalAPIClient {
    private static final String BASE_URL = "http://localhost:8000";
    private final OkHttpClient httpClient;

    public LocalAPIClient() {
        this.httpClient = new OkHttpClient();
    }

    /**
     * 모든 사용자 조회
     */
    public void getAllUsers() throws IOException {
        System.out.println("\n=== 모든 사용자 조회 ===");
        Request request = new Request.Builder()
            .url(BASE_URL + "/api/users")
            .get()
            .build();

        executeAndPrint(request);
    }

    /**
     * 특정 사용자 조회
     */
    public void getUserById(int userId) throws IOException {
        System.out.println("\n=== 사용자 ID " + userId + " 조회 ===");
        Request request = new Request.Builder()
            .url(BASE_URL + "/api/users/" + userId)
            .get()
            .build();

        executeAndPrint(request);
    }

    /**
     * 새 사용자 생성
     */
    public void createUser(String name, String email, int age) throws IOException {
        System.out.println("\n=== 새 사용자 생성: " + name + " ===");
        
        JSONObject userJson = new JSONObject();
        userJson.put("name", name);
        userJson.put("email", email);
        userJson.put("age", age);

        RequestBody body = RequestBody.create(
            userJson.toString(),
            MediaType.parse("application/json; charset=utf-8")
        );

        Request request = new Request.Builder()
            .url(BASE_URL + "/api/users")
            .post(body)
            .build();

        executeAndPrint(request);
    }

    /**
     * 사용자 정보 수정
     */
    public void updateUser(int userId, String name, String email, int age) throws IOException {
        System.out.println("\n=== 사용자 " + userId + " 정보 수정 ===");
        
        JSONObject userJson = new JSONObject();
        userJson.put("name", name);
        userJson.put("email", email);
        userJson.put("age", age);

        RequestBody body = RequestBody.create(
            userJson.toString(),
            MediaType.parse("application/json; charset=utf-8")
        );

        Request request = new Request.Builder()
            .url(BASE_URL + "/api/users/" + userId)
            .put(body)
            .build();

        executeAndPrint(request);
    }

    /**
     * 사용자 삭제
     */
    public void deleteUser(int userId) throws IOException {
        System.out.println("\n=== 사용자 " + userId + " 삭제 ===");
        
        Request request = new Request.Builder()
            .url(BASE_URL + "/api/users/" + userId)
            .delete()
            .build();

        executeAndPrint(request);
    }

    /**
     * 모든 작업 조회 (선택: 특정 사용자의 작업만)
     */
    public void getTasks(Integer userId) throws IOException {
        System.out.println("\n=== 작업 조회" + (userId != null ? " (사용자 " + userId + ")" : "") + " ===");
        
        String url = BASE_URL + "/api/tasks";
        if (userId != null) {
            url += "?user_id=" + userId;
        }

        Request request = new Request.Builder()
            .url(url)
            .get()
            .build();

        executeAndPrint(request);
    }

    /**
     * 특정 작업 조회
     */
    public void getTaskById(int taskId) throws IOException {
        System.out.println("\n=== 작업 ID " + taskId + " 조회 ===");
        
        Request request = new Request.Builder()
            .url(BASE_URL + "/api/tasks/" + taskId)
            .get()
            .build();

        executeAndPrint(request);
    }

    /**
     * 새 작업 생성
     */
    public void createTask(String title, String description, boolean completed, int userId) throws IOException {
        System.out.println("\n=== 새 작업 생성: " + title + " ===");
        
        JSONObject taskJson = new JSONObject();
        taskJson.put("title", title);
        taskJson.put("description", description);
        taskJson.put("completed", completed);
        taskJson.put("user_id", userId);

        RequestBody body = RequestBody.create(
            taskJson.toString(),
            MediaType.parse("application/json; charset=utf-8")
        );

        Request request = new Request.Builder()
            .url(BASE_URL + "/api/tasks")
            .post(body)
            .build();

        executeAndPrint(request);
    }

    /**
     * 작업 상태 업데이트
     */
    public void updateTaskStatus(int taskId, boolean completed) throws IOException {
        System.out.println("\n=== 작업 " + taskId + " 상태 업데이트 (완료: " + completed + ") ===");
        
        Request request = new Request.Builder()
            .url(BASE_URL + "/api/tasks/" + taskId + "?completed=" + completed)
            .patch(RequestBody.create("", null))
            .build();

        executeAndPrint(request);
    }

    /**
     * 서버 상태 확인
     */
    public void checkHealth() throws IOException {
        System.out.println("\n=== 서버 상태 확인 ===");
        
        Request request = new Request.Builder()
            .url(BASE_URL + "/health")
            .get()
            .build();

        executeAndPrint(request);
    }

    /**
     * HTTP 요청 실행 및 결과 출력
     */
    private void executeAndPrint(Request request) throws IOException {
        try (Response response = httpClient.newCall(request).execute()) {
            String responseBody = response.body() != null ? response.body().string() : "";
            
            System.out.println("상태 코드: " + response.code() + " " + response.message());
            System.out.println("응답 본문:");
            
            // JSON 예쁘게 출력
            try {
                Object json = new org.json.JSONTokener(responseBody).nextValue();
                if (json instanceof JSONObject) {
                    System.out.println(((JSONObject) json).toString(2));
                } else if (json instanceof JSONArray) {
                    System.out.println(((JSONArray) json).toString(2));
                } else {
                    System.out.println(responseBody);
                }
            } catch (Exception e) {
                System.out.println(responseBody);
            }
        }
    }

    /**
     * 메인 메서드 - 모든 API 호출 테스트
     */
    public static void main(String[] args) {
        LocalAPIClient client = new LocalAPIClient();

        try {
            // 서버 상태 확인
            client.checkHealth();

            // 사용자 관련 API
            System.out.println("\n\n╔════════════════════════════════════════╗");
            System.out.println("║          사용자 API 테스트             ║");
            System.out.println("╚════════════════════════════════════════╝");

            client.getAllUsers();
            client.getUserById(1);
            client.createUser("Emma", "emma@example.com", 26);
            client.updateUser(1, "Alice Smith", "alice.smith@example.com", 29);
            client.getUserById(1);

            // 작업 관련 API
            System.out.println("\n\n╔════════════════════════════════════════╗");
            System.out.println("║          작업 API 테스트               ║");
            System.out.println("╚════════════════════════════════════════╝");

            client.getTasks(null);
            client.getTasks(1);
            client.getTaskById(1);
            client.createTask("개발 완료", "Java API 클라이언트 개발", false, 1);
            client.updateTaskStatus(1, true);

            // 삭제 테스트
            System.out.println("\n\n╔════════════════════════════════════════╗");
            System.out.println("║            삭제 API 테스트             ║");
            System.out.println("╚════════════════════════════════════════╝");

            client.deleteUser(3);

            // 최종 상태
            System.out.println("\n\n╔════════════════════════════════════════╗");
            System.out.println("║          최종 서버 상태                ║");
            System.out.println("╚════════════════════════════════════════╝");

            client.checkHealth();

        } catch (IOException e) {
            System.err.println("API 호출 중 오류 발생:");
            e.printStackTrace();
            System.out.println("\n⚠️  로컬 API 서버가 실행 중인지 확인하세요!");
            System.out.println("   Python에서 다음 명령으로 실행: python api_server.py");
        }
    }
}
