/*------------------------------------------------------------------------------
Archivo: mainsproject.s
Microcontrolador: PIC16F887
Autor: Andy Bonilla
Compilador: pic-as (v2.30), MPLABX v5.45
    
Programa: laboratorio 5
Hardware: PIC16F887
    
Creado: 15 de agosto de 2021    
Descripcion: 
------------------------------------------------------------------------------*/

// CONFIG1
#pragma config FOSC = INTRC_NOCLKOUT   //configuracion de oscilador interno
#pragma config WDTE = OFF       // Watchdog Timer Enable bit (WDT disabled and can be enabled by SWDTEN bit of the WDTCON register)
#pragma config PWRTE = OFF      // Power-up Timer Enable bit (PWRT disabled)
#pragma config MCLRE = OFF      // RE3/MCLR pin function select bit (RE3/MCLR pin function is digital input, MCLR internally tied to VDD)
#pragma config CP = OFF         // Code Protection bit (Program memory code protection is disabled)
#pragma config CPD = OFF        // Data Code Protection bit (Data memory code protection is disabled)
#pragma config BOREN = OFF      // Brown Out Reset Selection bits (BOR disabled)
#pragma config IESO = OFF       // Internal External Switchover bit (Internal/External Switchover mode is disabled)
#pragma config FCMEN = OFF      // Fail-Safe Clock Monitor Enabled bit (Fail-Safe Clock Monitor is disabled)
#pragma config LVP = OFF        // Low Voltage Programming Enable bit (RB3 pin has digital I/O, HV on MCLR must be used for programming)

// CONFIG2
#pragma config BOR4V = BOR40V   // Brown-out Reset Selection bit (Brown-out Reset set to 4.0V)
#pragma config WRT = OFF        // Flash Program Memory Self Write Enable bits (Write protection off)

// #pragma config statements should precede project file includes.
// Use project enums instead of #define for ON and OFF.

/*-----------------------------------------------------------------------------
 ----------------------------LIBRERIAS-----------------------------------------
 -----------------------------------------------------------------------------*/
#include <stdint.h>
#include <pic16f887.h>
#include <xc.h>
#include <proc/pic16f887.h>
#include "Osc_config.h"
#include "UART_CONFIG.h"

/*-----------------------------------------------------------------------------
 ----------------------- VARIABLES A IMPLEMTENTAR------------------------------
 -----------------------------------------------------------------------------*/

//-------DIRECTIVAS DEL COMPILADOR
#define _XTAL_FREQ 4000000

//-------VARIABLES DE PROGRAMA
unsigned char antirrebote1;
unsigned char antirrebote2;
unsigned char cuenta;
unsigned char cen_cuenta, dec_cuenta, un_cuenta;
unsigned char cen_mandar, dec_mandar, un_mandar;
unsigned char cuenta_uart;
/*-----------------------------------------------------------------------------
 ------------------------ PROTOTIPOS DE FUNCIONES ------------------------------
 -----------------------------------------------------------------------------*/
void setup(void);
void mapeos(void);
void mandar_datos(void);
/*-----------------------------------------------------------------------------
 --------------------------- INTERRUPCIONES -----------------------------------
 -----------------------------------------------------------------------------*/
void __interrupt() isr(void) //funcion de interrupciones
{
    //-------INTERRUPCION POR BOTONAZO
    if (INTCONbits.RBIF)
    {
        switch(PORTB)
        {
            default:
                antirrebote1=0;
                antirrebote2=0;
                break;
                
            case(0b11111110):
                antirrebote1=1;
                break;
                
            case(0b11111101):
                antirrebote2=1;
                break;
        }
        INTCONbits.RBIF=0;
    }
    //-------INTERRUPCION POR COMUNICACION UART
    if (PIR1bits.TXIF)
    {
        cuenta_uart++;      //se suma variable guia
        mandar_datos();     //invoco funcion para mandar uart
        PIR1bits.TXIF=0;    //apago interrupcion
    }  
}
/*-----------------------------------------------------------------------------
 ----------------------------- MAIN LOOP --------------------------------------
 -----------------------------------------------------------------------------*/
void main(void)
{
    //-------CONFIGURACION DE PIC
    setup();
    
    while(1)
    {
        //-------ANTIRREBOTES DE BOTON 1
        if (antirrebote1==1 && PORTBbits.RB0==0  )
        {
            cuenta++;
            antirrebote1=0;
        }
        //-------ANTIRREBOTES DE BOTON 2
        if (antirrebote2==1 && PORTBbits.RB1==0  )
        {
            cuenta--;
            antirrebote2=0;
        }
        //-------
        if (cuenta>255 || cuenta <0)    //restringir el rango de variable
            cuenta=0;
        
        PORTD=cuenta;
        mapeos();
    }
   
}
/*-----------------------------------------------------------------------------
 ---------------------------------- SET UP -----------------------------------
 -----------------------------------------------------------------------------*/
void setup(void)
{
    //-------CONFIGURACION ENTRADAS ANALOGICAS
    ANSEL=0;
    ANSELH=0;
    //-------CONFIGURACION IN/OUT
    TRISBbits.TRISB0=1;                 //entrada para boton de suma
    TRISBbits.TRISB1=1;                 //entrada para boton de resta
    TRISD=0x00;                         //portD como salida de leds
   
    //-------LIMPIEZA DE PUERTOS
    PORTB=0;
    PORTD=0;
    //-------CONFIGURACION DE RELOJ A 4MHz
    osc_config(4);
    //-------CONFIGURACION DE COMUNICACION UART
    uart_config();                       
    //-------CONFIGURACION DE WPUB
    OPTION_REGbits.nRBPU=0;             //se activan WPUB
    WPUBbits.WPUB0=1;                   //RB0, boton de suma
    WPUBbits.WPUB1=1;                   //RB1, boton de resta
    
    //-------CONFIGURACION DE INTERRUPCIONES
    INTCONbits.GIE=1;           //se habilita interrupciones globales
    INTCONbits.PEIE=1;          //habilitan interrupciones por perifericos
    INTCONbits.RBIE=1;          //se  habilita IntOnChange B
    INTCONbits.RBIF=0;          //se  apaga bandera IntOnChange B
    IOCBbits.IOCB0=1;           //habilita IOCB RB0
    IOCBbits.IOCB1=1;           //habilita IOCB RB1
    PIE1bits.TXIE=1;            //enable interrupcion de tx uart
    //PIE1bits.RCIE=1;            //enable interrupcion de rx uart
    PIR1bits.TXIF=0;            //apago bandera interrupcion tx uart
    //PIR1bits.RCIF=0;            //apago bandera interrupcion rx uart*/
}
/*-----------------------------------------------------------------------------
 --------------------------------- FUNCIONES ----------------------------------
 -----------------------------------------------------------------------------*/
//-------FUNCION PARA MAPEOS DE VARIABLES
void mapeos(void)
{
    //-------MAPEO DE CENTENAS, DECENAS Y UNIDADES
    cen_cuenta=(((cuenta)/100)%10);    //centenas de pot1
    dec_cuenta=(((cuenta)/10)%10);    //centenas de pot1
    un_cuenta=((cuenta)%10);    //centenas de pot1
    //-------MAPEO DE VALORES ASCII
    cen_mandar=(cen_cuenta+0x30);
    dec_mandar=(dec_cuenta+0x30);
    un_mandar=(un_cuenta+0x30);
}
//-------FUNCION PARA MANDAR VALORES ASCII
void mandar_datos(void)
{
    switch(cuenta_uart)
    {
        case(1):
            TXREG=cen_mandar;    //mando centenas de cuenta botones
            break;
        case(2):
            TXREG=dec_mandar;    //mando decenas de cuenta botones
            break;
        case(3):
            TXREG=un_mandar;     //mando unidades de cuenta botones
            break;
        case(4):
            TXREG=44;            //separador de coma
            break;
        case(20):
            cuenta_uart=0;          //un tipo de delay para reiniciar cuenta
            break;
    }
}