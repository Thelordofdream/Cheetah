//
//  ViewController.m
//  Cheetah
//
//  Created by 张铭杰 on 26/1/18.
//  Copyright © 2018年 张铭杰. All rights reserved.
//

#import "ViewController.h"
#import "SYYHuobiNetHandler.h"

@implementation ViewController


- (void)viewDidLoad {
    [super viewDidLoad];
    
    // Do any additional setup after loading the view.
    
    // initializing
    srand((unsigned)time(NULL));
    market_usdt.dataSource = self;
    market_usdt.delegate = self;
    wallet.dataSource = self;
    wallet.delegate = self;
    invest.dataSource = self;
    invest.delegate = self;
    order.dataSource = self;
    order.delegate =self;
//    order_data = [NSMutableDictionary dictionary];
//    order_symbol = [order_data allKeys];
   
    // get the path of Documents
    NSString *docPath = [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) lastObject];
    // create the store path of the dictionary
    initFilePath = [docPath stringByAppendingPathComponent:@"init_data.txt"];
    NSFileManager *fm = [NSFileManager defaultManager];
    if([fm fileExistsAtPath:initFilePath]){
        NSLog(@"File exists");
        NSDictionary *init_data = [NSMutableDictionary dictionaryWithContentsOfFile:initFilePath];
        usdcny.stringValue = init_data[@"usdcny"];
        principal.stringValue = init_data[@"principal"];
    }
    else{
        NSLog(@"File doesn't exist");
        NSDictionary *init_data = [NSMutableDictionary dictionaryWithObjectsAndKeys:usdcny.stringValue, @"usdcny",principal.stringValue, @"principal", nil];
        [init_data writeToFile:initFilePath atomically:YES];
    }
    
    investFilePath = [docPath stringByAppendingPathComponent:@"invest_data.txt"];
    if([fm fileExistsAtPath:investFilePath]){
        NSLog(@"File exists");
        invest_data = [NSMutableDictionary dictionaryWithContentsOfFile:investFilePath];
        invest_symbol = [invest_data allKeys];
    }
    else{
        NSLog(@"File doesn't exist");
        invest_data = [NSMutableDictionary dictionary];
        [invest_data writeToFile:investFilePath atomically:YES];
    }
    
    // market data
    [SYYHuobiNetHandler requestSymbolsWithTag:(id)self succeed:^(id symbols) {
        market_data= [NSMutableDictionary dictionaryWithObjectsAndKeys:[NSMutableDictionary dictionary], @"usdt", [NSMutableDictionary dictionary], @"btc", [NSMutableDictionary dictionary], @"eth", nil];
        for(NSDictionary *each_symbol in symbols[@"data"]){
            NSMutableDictionary *symbol = [@{@"symbol":each_symbol[@"base-currency"], @"quote": each_symbol[@"quote-currency"], @"price":@"", @"hour":@"", @"quarter":@"", @"minute":@"", @"fluctuation_short":@"",@"fluctuation_mid":@"", @"amount-precision":each_symbol[@"amount-precision"], @"price-precision":each_symbol[@"price-precision"]}mutableCopy];
            [market_data[each_symbol[@"quote-currency"]] setObject:symbol forKey:each_symbol[@"base-currency"]];
        }
        
        NSThread *market_hour_thread_usdt = [[NSThread alloc] initWithTarget:self selector:@selector(market_hour_update:) object:market_data[@"usdt"]];
        [market_hour_thread_usdt start];

        NSThread *market_quarter_thread_usdt = [[NSThread alloc] initWithTarget:self selector:@selector(market_quarter_update:) object:market_data[@"usdt"]];
        [market_quarter_thread_usdt start];

        NSThread *market_minute_thread_usdt = [[NSThread alloc] initWithTarget:self selector:@selector(market_minute_update:) object:market_data[@"usdt"]];
        [market_minute_thread_usdt start];
        
        market_symbol_usdt = [market_data[@"usdt"] allKeys];
    } failed:^(id error) {
        NSLog(@"%@",error);
    }];
    
    // wallet data
    [SYYHuobiNetHandler requestAccountsWithTag:self succeed:^(id account_info) {
        NSString *account_id = account_info[@"data"][0][@"id"];
        account.stringValue = [NSString stringWithFormat:@"%@", account_id];
        
        NSThread *wallet_thread = [[NSThread alloc] initWithTarget:self selector:@selector(wallet_update:) object:account_id];
        [wallet_thread start];
    } failed:^(id error) {
        NSLog(@"%@",error);
    }];
    
    //    [SYYHuobiNetHandler requestTimestampWithTag:(id)self succeed:^(id date_info) {
    //        NSLog(@"%@", date_info);
    //        NSTimeInterval time = [date_info[@"data"] doubleValue] / 1000;
    //        NSDate *detaildate=[NSDate dateWithTimeIntervalSince1970:time];
    //        NSLog(@"%@", [detaildate description]);
    //    } failed:^(id error) {
    //
    //    }];
    
    //UI updating
    
    UItimer1 =  [NSTimer scheduledTimerWithTimeInterval:0.5 target:self selector:@selector(updateUI1) userInfo:nil repeats:YES];
    [UItimer1 setFireDate:[NSDate distantPast]];
    
    //data updating
    
    NSThread *invest_thread = [[NSThread alloc] initWithTarget:self selector:@selector(invest_update:) object:nil];
    [invest_thread start];
    
//    NSThread *order_thread = [[NSThread alloc] initWithTarget:self selector:@selector(order_update:) object:nil];
//    [order_thread start];
}

// UI updating
- (void) updateUI1{
    [market_usdt reloadData];
    [wallet reloadData];
    [invest reloadData];
//    [order reloadData];
}

// Wallet Data updating
- (void) wallet_update:(NSString *) account_id{
    while(true){
        [SYYHuobiNetHandler requestAccountBalanceWithTag:self accountId:account_id succeed:^(id balance_info) {
            float sum = 0.0;
//            float btc = 0.0;
            wallet_data = [NSMutableDictionary dictionary];
            for(NSDictionary *each_currency in balance_info[@"data"][@"list"]){
                if([each_currency[@"balance"] floatValue] != 0){
                    NSMutableDictionary *symbol = [@{@"currency":each_currency[@"currency"], @"balance":[NSString stringWithFormat:@"%.8f", [each_currency[@"balance"] floatValue]], @"price":@"", @"state":each_currency[@"type"]} mutableCopy];
                    [wallet_data setObject:symbol forKey:each_currency[@"currency"]];
                    if(market_data[@"usdt"][each_currency[@"currency"]][@"price"] != NULL){
                        wallet_data[each_currency[@"currency"]][@"price"] = market_data[@"usdt"][each_currency[@"currency"]][@"price"];
                        sum += [market_data[@"usdt"][each_currency[@"currency"]][@"price"] floatValue] * [each_currency[@"balance"] floatValue];
                    }
                    else if([each_currency[@"currency"] isEqual:@"usdt"])
                    {
                        sum += [each_currency[@"balance"] floatValue];
                    }
                }
            }
            usd.stringValue = [NSString stringWithFormat:@"%.8f", sum];
            cny.stringValue = [NSString stringWithFormat:@"%.2f", sum * [usdcny.stringValue floatValue]];
            profit.stringValue = [NSString stringWithFormat:@"%.2f", ((sum * [usdcny.stringValue floatValue] - [principal.stringValue floatValue])/ [principal.stringValue floatValue] * 100)];
            if(market_data[@"usdt"][@"btc"][@"price"] != NULL){
                btc.stringValue = [NSString stringWithFormat:@"%.8f", sum / [market_data[@"usdt"][@"btc"][@"price"] floatValue]];
                btcusdt.stringValue = [NSString stringWithFormat:@"%.2f", [market_data[@"usdt"][@"btc"][@"price"] floatValue]];
            }
            wallet_symbol = [wallet_data allKeys];
        } failed:^(id error) {
            NSLog(@"%@",error);
        }];
        
        [NSThread sleepForTimeInterval:2];
    }
}

// Invest Data updating
- (void) invest_update:(NSString *)sender{
    while(true){
        for(NSString *symbol in invest_data){
            if(market_data[@"usdt"][symbol][@"price"] != NULL)
            {
                [invest_data[symbol] setObject:market_data[@"usdt"][symbol][@"price"] forKey:@"price"];
                NSString *balance = @"";
                NSString *profit = @"";
                if(wallet_data[symbol][@"balance"] != NULL)
                {
                    balance = [NSString stringWithFormat:[[@"\%." stringByAppendingString: [NSString stringWithFormat:@"%@", market_data[@"usdt"][symbol][@"amount-precision"]]] stringByAppendingString:@"f"], [wallet_data[symbol][@"balance"] floatValue]];
                    
                    profit = [[NSString stringWithFormat:@"%.2f",([invest_data[symbol][@"price"] floatValue] * [balance floatValue] * 0.998 - [invest_data[symbol][@"cost"] floatValue] * [invest_data[symbol][@"amount"] floatValue]) / ([invest_data[symbol][@"cost"] floatValue] * [invest_data[symbol][@"amount"] floatValue]) * 100] stringByAppendingString:@"%"];
                }
                [invest_data[symbol] setObject:balance forKey:@"balance"];
                [invest_data[symbol] setObject:profit forKey:@"profit"];
            }
        }
        [NSThread sleepForTimeInterval:2];
    }
}

// Order Data updating
- (void) order_update:(NSString *)sender{
    while(true){
        
    }
}

// Market Data updating
- (void) market_day_update:(NSDictionary *) symbols{
    while(true){
        for(NSDictionary *each_symbol in symbols){
            [SYYHuobiNetHandler requestHistoryKlineWithTag:self symbol:[symbols[each_symbol][@"symbol"] stringByAppendingString:symbols[each_symbol][@"quote"]] period:@"1day" size:@"1" succeed:^(id day_info) {
                [market_data[symbols[each_symbol][@"quote"]][each_symbol] setValue:[[self calculate_change:day_info[@"data"][0]] stringByAppendingString:@"%"] forKey:@"day"];
            } failed:^(id error) {
//                NSLog(@"%@",error);
            }];
        }
        [NSThread sleepForTimeInterval:20];
    }
}

- (void) market_hour_update:(NSDictionary *) symbols{
    while(true){
        for(NSDictionary *each_symbol in symbols){
            [SYYHuobiNetHandler requestHistoryKlineWithTag:self symbol:[symbols[each_symbol][@"symbol"] stringByAppendingString:symbols[each_symbol][@"quote"]] period:@"60min" size:@"2" succeed:^(id hour_info) {
                [market_data[symbols[each_symbol][@"quote"]][each_symbol] setValue:[[self calculate_change:hour_info[@"data"][0]] stringByAppendingString:@"%"] forKey:@"hour"];
                NSString *fluctuation_mid = [self calculate_fluctuation:hour_info[@"data"]];
                [market_data[symbols[each_symbol][@"quote"]][each_symbol] setValue:[fluctuation_mid stringByAppendingString:@"%"] forKey:@"fluctuation_mid"];
            } failed:^(id error) {
//                NSLog(@"%@",error);
            }];
        }
        [NSThread sleepForTimeInterval:5];
    }
}

- (void) market_quarter_update:(NSDictionary *) symbols{
    while(true){
        for(NSDictionary *each_symbol in symbols){
            [SYYHuobiNetHandler requestHistoryKlineWithTag:self symbol:[symbols[each_symbol][@"symbol"] stringByAppendingString:symbols[each_symbol][@"quote"]] period:@"15min" size:@"2" succeed:^(id quarter_info) {
                [market_data[symbols[each_symbol][@"quote"]][each_symbol] setValue:[[self calculate_change:quarter_info[@"data"][0]] stringByAppendingString:@"%"] forKey:@"quarter"];
                NSString *fluctuation_short = [self calculate_fluctuation:quarter_info[@"data"]];
                [market_data[symbols[each_symbol][@"quote"]][each_symbol] setValue:[fluctuation_short stringByAppendingString:@"%"] forKey:@"fluctuation_short"];
            } failed:^(id error) {
//                NSLog(@"%@",error);
            }];
        }
        [NSThread sleepForTimeInterval:2];
    }
}

- (void) market_minute_update:(NSDictionary *) symbols{
    while(true){
        for(NSDictionary *each_symbol in symbols){
            [SYYHuobiNetHandler requestHistoryKlineWithTag:self symbol:[symbols[each_symbol][@"symbol"] stringByAppendingString:symbols[each_symbol][@"quote"]] period:@"1min" size:@"1" succeed:^(id minute_info) {
                [market_data[symbols[each_symbol][@"quote"]][each_symbol] setValue:[[self calculate_change:minute_info[@"data"][0]] stringByAppendingString:@"%"] forKey:@"minute"];
                [market_data[symbols[each_symbol][@"quote"]][each_symbol] setValue:minute_info[@"data"][0][@"close"] forKey:@"price"];
            } failed:^(id error) {
//                NSLog(@"%@",error);
            }];
        }
        [NSThread sleepForTimeInterval:2];
    }
}

// funcational methods
- (NSString *) calculate_change:(NSDictionary *) kline
{
    float close = [kline[@"close"] floatValue];
    float open = [kline[@"open"] floatValue];
    return [NSString stringWithFormat:@"%.2f", ((close - open) / open * 100.0)];
}

- (NSString *) calculate_fluctuation:(NSArray *) kline
{
    float high1 = [kline[0][@"high"] floatValue];
    float high2 = [kline[1][@"high"] floatValue];
    float low1 = [kline[0][@"low"] floatValue];
    float low2 = [kline[1][@"low"] floatValue];
    float fluctuation1 = (high1 - low2) / low2;
    float fluctuation2 = (low1 - high2) / high2;
    if(fabs(fluctuation1) >= fabs(fluctuation2))
    {
        return [NSString stringWithFormat:@"%.2f", fluctuation1 * 100];
    }
    else
        return [NSString stringWithFormat:@"%.2f", fluctuation2 * 100];
}

// Table action
- (NSInteger)numberOfRowsInTableView:(NSTableView *)tableView {
    if(tableView == market_usdt)
        return [market_data[@"usdt"] count];
    else if(tableView == wallet)
        return [wallet_data count];
    else if(tableView == invest)
        return [invest_data count];
//    else if(tableView == order)
//        return [order_data count];
    else
        return 0;
}

- (id)tableView:(NSTableView *)tableView objectValueForTableColumn:(NSTableColumn *)tableColumn row:(NSInteger)row
{
    if(tableView == market_usdt)
        return market_data[@"usdt"][market_symbol_usdt[row]][tableColumn.identifier];
    else if(tableView == wallet)
        return wallet_data[wallet_symbol[row]][tableColumn.identifier];
    else if(tableView == invest)
        return invest_data[invest_symbol[row]][tableColumn.identifier];
//    else if(tableView == order)
//        return invest_data[order_symbol[row]][tableColumn.identifier];
    else
        return @"N/A";
}

- (BOOL)tableView:(NSTableView *)tableView shouldEditTableColumn:(NSTableColumn *)tableColumn row:(NSInteger)row
{
    return NO;
}

// Button action
-(IBAction)store:(id)sender{
    NSDictionary *init_data = [NSMutableDictionary dictionaryWithObjectsAndKeys:usdcny.stringValue, @"usdcny",principal.stringValue, @"principal", nil];
    [init_data writeToFile:initFilePath atomically:YES];
}

- (IBAction)watch:(id)sender{
    if(market_data[@"usdt"][currency.stringValue] != NULL)
    {
        NSMutableDictionary *symbol = [@{@"symbol":currency.stringValue, @"amount":amount.stringValue,
                                         @"balance":@"",@"cost":cost.stringValue, @"pirce":@"", @"profit":@""} mutableCopy];
        [invest_data setObject:symbol forKey:currency.stringValue];
        invest_symbol = [invest_data allKeys];
        [invest_data writeToFile:investFilePath atomically:YES];
    }
}

// TextField action


- (void)setRepresentedObject:(id)representedObject {
    [super setRepresentedObject:representedObject];
    
    // Update the view, if already loaded.
}


@end
