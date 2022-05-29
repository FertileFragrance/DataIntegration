import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class search {
    public static void main(String[] args){
        File csv = new File("/home/wcy/桌面/数据集成/loan/result.csv"); // CSV文件路径
        File csvout = new File("/home/wcy/桌面/数据集成/loan/out.csv"); // CSV文件路径
        BufferedReader brin = null;
        BufferedWriter brout = null;
        try {
            brin = new BufferedReader(new FileReader(csv));
            brout = new BufferedWriter(new FileWriter(csvout));
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        ;
        String line = "";
        String res = "";
        String line1 = null;
        List<String[]> res0 = new ArrayList<String[]>();
//        ArrayList<Integer> scores = new ArrayList<>();
        try {
            line1 = brin.readLine();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        String[] lineSplit1 = line1.split(",");
        for(int i = 0; i < lineSplit1.length; i++){
            System.out.print(i);
            System.out.println(" " + lineSplit1[i]);
        }
        int count = 0;
        while (true){
            try {
                if (!((line = brin.readLine()) != null)) break;
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            String[] lineSplit = line.split(",");
            int score = 60;
            int overdue_times_90l = Integer.valueOf(lineSplit[113]); //还款逾期不超过90天次数
            int overdue_times_90g = Integer.valueOf(lineSplit[114]); //还款逾期超过90天次数
            int owed_int_times_90l = Integer.valueOf(lineSplit[111]); //欠息逾期不超过90天次数
            int owed_int_times_90g = Integer.valueOf(lineSplit[112]); //欠息逾期超过90天次数
            if ((overdue_times_90l + overdue_times_90g * 2 + owed_int_times_90l + owed_int_times_90g * 2) > 8) {
                continue;
            }
            score = score - (overdue_times_90l + overdue_times_90g * 2 + owed_int_times_90l + owed_int_times_90g * 2) * 3;
            int is_black = Integer.valueOf(lineSplit[121]); //是否黑名单
            if(is_black == 1){
                continue;
            }
            int age = Integer.valueOf(lineSplit[121]); //年龄
            float cust_all_bal_sum = Float.valueOf(lineSplit[97]); //可用资产
            if(cust_all_bal_sum >= 50000.0 && cust_all_bal_sum <= 200000.0){
                score += 10;
            }
            else if(cust_all_bal_sum > 200000.0 && cust_all_bal_sum <= 1000000){
                score += 8;
            }
            else {
                score += 2;
            }
            float contract_buy_car_time = Float.valueOf(lineSplit[30]); //贷款买车次数
            float contract_buy_house_time = Float.valueOf(lineSplit[33]); //贷款买房次数
            float has_car_etc = Float.valueOf(lineSplit[65]); //是否有etc消费
            int marrige = Integer.valueOf(lineSplit[123]); //婚姻状况
            int sex = Integer.valueOf(lineSplit[120]);//性别
            if(contract_buy_car_time == 0.0 && has_car_etc == 0.0){
                if(age >= 22 && age <= 35){
                    score += 6;
                    if(marrige == 1){
                        score += 2;
                    } else if(marrige == 2) {
                        score += 4;
                    }
                    if(sex == 1){
                        score += 2;
                    }
                } else if(age > 35 && age <= 48) {
                    score += 6;
                } else if(age > 54 && age <= 60 && marrige == 2) {
                    score += 5;
                }
            }
            if(contract_buy_house_time == 0.0){
                if(age >= 22 && age <= 35){
                    score += 12;
                    if(marrige == 1){
                        score += 3;
                    } else if(marrige == 2) {
                        score += 5;
                    }
                    if(sex == 1){
                        score += 3;
                    }
                } else if(age > 35 && age <= 48) {
                    score += 5;
                } else if(age > 54 && age <= 60 && marrige == 2) {
                    score += 7;
                }
            }
            else{
            	if(age >= 22 && age <= 35){
                    score += 4;
                    if(marrige == 1){
                        score += 1;
                    } else if(marrige == 2) {
                        score += 2;
                    }
                    if(sex == 1){
                        score += 1;
                    }
                } else if(age > 35 && age <= 48) {
                    score += 2;
                } else if(age > 54 && age <= 60 && marrige == 2) {
                    score += 2;
                }
            }
//            scores.add(score);
            if(score > 90) {
                count++;
                res0.add(lineSplit);
                res = lineSplit[0];
//                try {
//                    brout.write(res);
//                    brout.write("\n");
//                } catch (IOException e) {
//                    throw new RuntimeException(e);
//                }
                System.out.println(res);
            }
//            res = lineSplit[0];
//            try {
//                brout.write(res);
//            } catch (IOException e) {
//                throw new RuntimeException(e);
//            }
//            System.out.println(res);
        }
//        for(int j = 0; j < scores.size(); j++){
//            if(scores.get(j) > 95) {
//                count++;
//                System.out.println(count);
//            }
//        }
        System.out.println(count);
    }


}
