#include <winsock2.h>
#include <iptypes.h>
#include <iphlpapi.h>
#include <windows.h>
#include <iostream>
#include <stdio.h>
#include <winnetwk.h>


#pragma comment(lib, "mpr.lib")
#pragma comment(lib, "netapi32.lib")

void DisplayStruct(int i, LPNETRESOURCE lpnrLocal);

typedef struct _ASTAT_  //струкутруа под информацию
{
    ADAPTER_STATUS adapt;
    NAME_BUFFER NameBuff[30];
}ASTAT, * PASTAT;
ASTAT Adapter;

void GetMacAddress()
{
    NCB Ncb;     
    UCHAR uRetCode; 
    LANA_ENUM lenum;


    memset(&Ncb, 0, sizeof(Ncb)); //выделение памяти под структуру
    Ncb.ncb_command = NCBENUM; //Команда NCBENUM позволяет получить список чисел LANA
    Ncb.ncb_buffer = (UCHAR*)&lenum;
    Ncb.ncb_length = sizeof(lenum);
    uRetCode = Netbios(&Ncb);//После подготовки данных и переменных можно выполнить команду NetBios

    for (int i = 0; i < lenum.length; i++) {
        memset(&Ncb, 0, sizeof(Ncb));
        Ncb.ncb_command = NCBRESET;//команда очищает имена и сеансы связи
        Ncb.ncb_lana_num = lenum.lana[i]; // адаптерный номер LAN

        uRetCode = Netbios(&Ncb); // вызов нетбоис для выполнения команды очистки

        memset(&Ncb, 0, sizeof(Ncb));
        Ncb.ncb_command = NCBASTAT; //Для получения адреса используется команда NCBASTAT с параметром - "* см строку 51
        Ncb.ncb_lana_num = lenum.lana[i];// адаптерный номер LAN

        strcpy_s((char*)Ncb.ncb_callname, sizeof(Ncb.ncb_callname), "* ");
        Ncb.ncb_buffer = (unsigned char*)&Adapter; // буфер это структура адаптера и укажем длину
        Ncb.ncb_length = sizeof(Adapter);

        uRetCode = Netbios(&Ncb);//После подготовки данных и переменных выполнить команду NetBios
        if (uRetCode == 0) { //Код возврата должен быть 0 при нормальном выполнении команды
            printf("The Ethernet Number on LANA %d is: % 02x % 02x % 02x % 02x % 02x % 02x\n",
                lenum.lana[i],
                Adapter.adapt.adapter_address[0],
                Adapter.adapt.adapter_address[1],
                Adapter.adapt.adapter_address[2],
                Adapter.adapt.adapter_address[3],
                Adapter.adapt.adapter_address[4],
                Adapter.adapt.adapter_address[5]);
        }

    }
}



BOOL WINAPI EnumerateFunc(LPNETRESOURCE lpnr)
{
    DWORD dwResult, dwResultEnum;
    HANDLE hEnum;// указатель на ресурсы
    DWORD cbBuffer = 16384;//количество байт для выделения
    DWORD cEntries = -1; 
    LPNETRESOURCE lpnrLocal;
    DWORD i;
    // Вызов функции WNetOpenEnum для начала перечисления компьютеров.
    //При успешном выполнении функция вернет NO_ERROR.
    dwResult = WNetOpenEnum(RESOURCE_GLOBALNET, // область применения.Перечисление  всех ресурсов в сети.
        RESOURCETYPE_ANY, // типы ресурсов для перечисления.все типы ресурсов
        0, //Тип использования ресурса для перечисления.Если lpNetResource равен нулю, то для перечисления будет начинаться с самого верха сети. В другом случае этот параметр должен быть заполнен.
        lpnr, //структура для информации о ресурсе
        &hEnum); // указатель на перечислитель
    if (dwResult != NO_ERROR)
    {
        // Обработка ошибок.
        printf("WnetOpenEnum failed with error %d\n", dwResult);
        return FALSE;
    }
    //Выделяет указанное количество байтов из кучи.
    lpnrLocal = (LPNETRESOURCE)GlobalAlloc(GPTR,// атрибут выделения памяти(выд фиксированной памяти и инициализация 0
        cbBuffer); // количество байт
    if (lpnrLocal == NULL) {
        printf("WnetOpenEnum failed with error %d\n", dwResult);
        return FALSE;
    }

    do
    {
        ZeroMemory(lpnrLocal, cbBuffer);
        dwResultEnum = WNetEnumResource(hEnum,// указатель на ресурсы
            &cEntries, // сколько перечислят и результат перечисления
            lpnrLocal, // указатель на буфер
            &cbBuffer);// размер буфера
        if (dwResultEnum == NO_ERROR)
        {
            for (i = 0; i < cEntries; i++)
            {
                DisplayStruct(i, &lpnrLocal[i]);
                if (RESOURCEUSAGE_CONTAINER == (lpnrLocal[i].dwUsage
                    & RESOURCEUSAGE_CONTAINER))
                    if (!EnumerateFunc(&lpnrLocal[i]))
                        printf("EnumerateFunc returned FALSE\n");
            }
        }
        // Обработка ошибок.
        else if (dwResultEnum != ERROR_NO_MORE_ITEMS)
        {
            printf("WNetEnumResource failed with error %d\n", dwResultEnum);
            break;
        }
    } while (dwResultEnum != ERROR_NO_MORE_ITEMS);
    GlobalFree((HGLOBAL)lpnrLocal);
    // Вызов WNetCloseEnum для остановки перечисления.Закрытие указателля на перечислитель
    dwResult = WNetCloseEnum(hEnum);
    if (dwResult != NO_ERROR)
    {
        // Обработка ошибок.
        printf("WNetCloseEnum failed with error %d\n", dwResult);
        return FALSE;
    }
    return TRUE;
}

void DisplayStruct(int i, LPNETRESOURCE lpnrLocal) // вывод структуры
{
    printf("NETRESOURCE[%d] Scope: ", i);
    switch (lpnrLocal->dwScope) {
    case (RESOURCE_CONNECTED):
        printf("connected\n");
        break;
    case (RESOURCE_GLOBALNET):
        printf("all resources\n");
        break;
    case (RESOURCE_REMEMBERED):
        printf("remembered\n");
        break;
    default:
        printf("unknown scope %d\n", lpnrLocal->dwScope);
        break;
    }

    printf("NETRESOURCE[%d] Type: ", i);
    switch (lpnrLocal->dwType) {
    case (RESOURCETYPE_ANY):
        printf("any\n");
        break;
    case (RESOURCETYPE_DISK):
        printf("disk\n");
        break;
    case (RESOURCETYPE_PRINT):
        printf("print\n");
        break;
    default:
        printf("unknown type %d\n", lpnrLocal->dwType);
        break;
    }

    printf("NETRESOURCE[%d] DisplayType: ", i);
    switch (lpnrLocal->dwDisplayType) {
    case (RESOURCEDISPLAYTYPE_GENERIC):
        printf("generic\n");
        break;
    case (RESOURCEDISPLAYTYPE_DOMAIN):
        printf("domain\n");
        break;
    case (RESOURCEDISPLAYTYPE_SERVER):
        printf("server\n");
        break;
    case (RESOURCEDISPLAYTYPE_SHARE):
        printf("share\n");
        break;
    case (RESOURCEDISPLAYTYPE_FILE):
        printf("file\n");
        break;
    case (RESOURCEDISPLAYTYPE_GROUP):
        printf("group\n");
        break;
    case (RESOURCEDISPLAYTYPE_NETWORK):
        printf("network\n");
        break;
    default:
        printf("unknown display type %d\n", lpnrLocal->dwDisplayType);
        break;
    }

    printf("NETRESOURCE[%d] Usage: 0x%x = ", i, lpnrLocal->dwUsage);
    if (lpnrLocal->dwUsage & RESOURCEUSAGE_CONNECTABLE)
        printf("connectable ");
    if (lpnrLocal->dwUsage & RESOURCEUSAGE_CONTAINER)
        printf("container ");
    printf("\n");

    printf("NETRESOURCE[%d] Localname: %S\n", i, lpnrLocal->lpLocalName);
    printf("NETRESOURCE[%d] Remotename: %S\n", i, lpnrLocal->lpRemoteName);
    printf("NETRESOURCE[%d] Comment: %S\n", i, lpnrLocal->lpComment);
    printf("NETRESOURCE[%d] Provider: %S\n", i, lpnrLocal->lpProvider);
    printf("\n");
}

 int main()
{
    printf("Getting the MAC Address: \n");
    GetMacAddress();

    printf("\nEnumerating Network Resources: \n");
    LPNETRESOURCE lpnr = NULL;

    if (EnumerateFunc(lpnr) == FALSE)
        printf("Call to EnumerateFunc failed\n");

    system("pause");
}