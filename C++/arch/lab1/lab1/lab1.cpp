#include <windows.h>

HINSTANCE hInst;
HWND hwnd;
RECT clientRect;
int posX = 100;
int posY = 100;
int radius = 30;
bool isCtrlPressed = false;

void DrawCircle(HDC hdc, int x, int y, int r) {
    Ellipse(hdc, x - r, y - r, x + r, y + r);
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam) {
    switch (message) {
    case WM_CREATE:
        GetClientRect(hwnd, &clientRect);
        break;

    case WM_PAINT: {
        PAINTSTRUCT ps;
        HDC hdc = BeginPaint(hwnd, &ps);

        DrawCircle(hdc, posX, posY, radius);

        EndPaint(hwnd, &ps);
        break;
    }

    case WM_MOUSEWHEEL: {
        int delta = GET_WHEEL_DELTA_WPARAM(wParam);
        if (delta > 0) {
            posY -= 10;
        }
        else if (delta < 0) {
            posY += 10;
        }

        InvalidateRect(hwnd, NULL, TRUE);
        break;
    }

    case WM_KEYDOWN:
        if (wParam == VK_CONTROL) {
            isCtrlPressed = true;
        }
        break;

    case WM_KEYUP:
        if (wParam == VK_CONTROL) {
            isCtrlPressed = false;
        }
        break;

    case WM_CHAR:
        if (isCtrlPressed) {
            if (wParam == 'A' || wParam == 'a') {
                posX -= 10;
            }
            else if (wParam == 'D' || wParam == 'd') {
                posX += 10;
            }

            InvalidateRect(hwnd, NULL, TRUE);
        }
        break;

    case WM_CLOSE:
        PostQuitMessage(0);
        break;

    default:
        return DefWindowProc(hwnd, message, wParam, lParam);
    }

    return 0;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    WNDCLASSEX wcex;
    wcex.cbSize = sizeof(WNDCLASSEX);
    wcex.style = CS_HREDRAW | CS_VREDRAW;
    wcex.lpfnWndProc = WndProc;
    wcex.cbClsExtra = 0;
    wcex.cbWndExtra = 0;
    wcex.hInstance = hInstance;
    wcex.hIcon = LoadIcon(hInstance, IDI_APPLICATION);
    wcex.hCursor = LoadCursor(NULL, IDC_ARROW);
    wcex.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wcex.lpszMenuName = NULL;
    wcex.lpszClassName = L"MyWindowClass";
    wcex.hIconSm = LoadIcon(wcex.hInstance, IDI_APPLICATION);

    if (!RegisterClassEx(&wcex)) {
        MessageBox(NULL, L"Error registering window class", L"Error", MB_ICONERROR);
        return 1;
    }

    hInst = hInstance;
    hwnd = CreateWindow(L"MyWindowClass", L"Graphics Program", WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 800, 600, NULL, NULL, hInstance, NULL);

    if (!hwnd) {
        MessageBox(NULL, L"Error creating window", L"Error", MB_ICONERROR);
        return 1;
    }

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return (int)msg.wParam;
}
