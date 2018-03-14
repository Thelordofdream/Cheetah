//
//  ViewController.h
//  Cheetah
//
//  Created by 张铭杰 on 26/1/18.
//  Copyright © 2018年 张铭杰. All rights reserved.
//

#import <Cocoa/Cocoa.h>

@interface ViewController : NSViewController
{
    __weak IBOutlet NSTableView *wallet;
    __weak IBOutlet NSTableView *order;
    __weak IBOutlet NSTableView *invest;
    __weak IBOutlet NSTableView *market_usdt;
    
    __weak IBOutlet NSTextField *account;
    __weak IBOutlet NSTextField *btc;
    __weak IBOutlet NSTextField *cny;
    __weak IBOutlet NSTextField *usd;
    __weak IBOutlet NSTextField *btcusdt;
    __weak IBOutlet NSTextField *profit;
    
    __weak IBOutlet NSTextField *usdcny;
    __weak IBOutlet NSTextField *principal;
    
    __weak IBOutlet NSTextField *currency;
    __weak IBOutlet NSTextField *amount;
    __weak IBOutlet NSTextField *cost;
    
//    __weak IBOutlet NSTextField *currency_trade;
//    __weak IBOutlet NSTextField *cost_trade;
//    __weak IBOutlet NSTextField *amount_trade;
    
    
    __weak IBOutlet NSButton *store;
    
    
    
    
    NSTimer *UItimer1;
    
    NSMutableDictionary *market_data;
    NSArray *market_symbol_usdt;
    
    NSMutableDictionary *wallet_data;
    NSArray *wallet_symbol;
    
    NSMutableDictionary *invest_data;
    NSArray *invest_symbol;
    
//    NSMutableDictionary *order_data;
//    NSArray *order_symbol;
    
    NSString *initFilePath;
    NSString *investFilePath;
    

}

@end
