import React, { useMemo, useState } from "react";
import { motion } from "framer-motion";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  BarChart,
  Bar,
  AreaChart,
  Area,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";

// Data source: "Initial Coldwater Creek 2025 Year in Review data - Copy.xlsx" (Sheet 1)
// Note: No numbers below are fabricated; they are parsed/aggregated from the uploaded file.
const DATA = {
  joinsMonthly: [
    { period: "2024-01", year: 2024, month: "Jan", Online: 7152, Phone: 593, Total: 7745 },
    { period: "2024-02", year: 2024, month: "Feb", Online: 6468, Phone: 701, Total: 7169 },
    { period: "2024-03", year: 2024, month: "Mar", Online: 7062, Phone: 709, Total: 7771 },
    { period: "2024-04", year: 2024, month: "Apr", Online: 9429, Phone: 905, Total: 10334 },
    { period: "2024-05", year: 2024, month: "May", Online: 13666, Phone: 888, Total: 14554 },
    { period: "2024-06", year: 2024, month: "Jun", Online: 12153, Phone: 539, Total: 12692 },
    { period: "2024-07", year: 2024, month: "Jul", Online: 9398, Phone: 478, Total: 9876 },
    { period: "2024-08", year: 2024, month: "Aug", Online: 10492, Phone: 602, Total: 11094 },
    { period: "2024-09", year: 2024, month: "Sep", Online: 11295, Phone: 718, Total: 12013 },
    { period: "2024-10", year: 2024, month: "Oct", Online: 11989, Phone: 975, Total: 12964 },
    { period: "2024-11", year: 2024, month: "Nov", Online: 17285, Phone: 1202, Total: 18487 },
    { period: "2024-12", year: 2024, month: "Dec", Online: 12124, Phone: 1017, Total: 13141 },
    { period: "2025-01", year: 2025, month: "Jan", Online: 8119, Phone: 736, Total: 8855 },
    { period: "2025-02", year: 2025, month: "Feb", Online: 9635, Phone: 869, Total: 10504 },
    { period: "2025-03", year: 2025, month: "Mar", Online: 12593, Phone: 999, Total: 13592 },
    { period: "2025-04", year: 2025, month: "Apr", Online: 16740, Phone: 1028, Total: 17768 },
    { period: "2025-05", year: 2025, month: "May", Online: 13285, Phone: 924, Total: 14209 },
    { period: "2025-06", year: 2025, month: "Jun", Online: 10863, Phone: 719, Total: 11582 },
    { period: "2025-07", year: 2025, month: "Jul", Online: 10060, Phone: 897, Total: 10957 },
    { period: "2025-08", year: 2025, month: "Aug", Online: 12346, Phone: 881, Total: 13227 },
    { period: "2025-09", year: 2025, month: "Sep", Online: 13487, Phone: 944, Total: 14431 },
    { period: "2025-10", year: 2025, month: "Oct", Online: 12873, Phone: 1241, Total: 14114 },
    { period: "2025-11", year: 2025, month: "Nov", Online: 16323, Phone: 1657, Total: 17980 },
    { period: "2025-12", year: 2025, month: "Dec", Online: 5170, Phone: 476, Total: 5646 },
  ],
  trialCancelMonthly: [
    { period: "2024-01", year: 2024, month: "Jan", Online: 0.1953, Phone: 0.403, Total: 0.2112 },
    { period: "2024-02", year: 2024, month: "Feb", Online: 0.209, Phone: 0.4294, Total: 0.2306 },
    { period: "2024-03", year: 2024, month: "Mar", Online: 0.1984, Phone: 0.4302, Total: 0.2195 },
    { period: "2024-04", year: 2024, month: "Apr", Online: 0.2025, Phone: 0.4276, Total: 0.2222 },
    { period: "2024-05", year: 2024, month: "May", Online: 0.2268, Phone: 0.4336, Total: 0.2394 },
    { period: "2024-06", year: 2024, month: "Jun", Online: 0.26, Phone: 0.4935, Total: 0.272 },
    { period: "2024-07", year: 2024, month: "Jul", Online: 0.2472, Phone: 0.5146, Total: 0.2622 },
    { period: "2024-08", year: 2024, month: "Aug", Online: 0.2167, Phone: 0.4778, Total: 0.2345 },
    { period: "2024-09", year: 2024, month: "Sep", Online: 0.1963, Phone: 0.4564, Total: 0.2129 },
    { period: "2024-10", year: 2024, month: "Oct", Online: 0.1991, Phone: 0.4595, Total: 0.2149 },
    { period: "2024-11", year: 2024, month: "Nov", Online: 0.1853, Phone: 0.486, Total: 0.2051 },
    { period: "2024-12", year: 2024, month: "Dec", Online: 0.1848, Phone: 0.4503, Total: 0.2041 },
    { period: "2025-01", year: 2025, month: "Jan", Online: 0.1972, Phone: 0.4075, Total: 0.2102 },
    { period: "2025-02", year: 2025, month: "Feb", Online: 0.2234, Phone: 0.4383, Total: 0.2367 },
    { period: "2025-03", year: 2025, month: "Mar", Online: 0.2273, Phone: 0.4737, Total: 0.2444 },
    { period: "2025-04", year: 2025, month: "Apr", Online: 0.217, Phone: 0.4537, Total: 0.2324 },
    { period: "2025-05", year: 2025, month: "May", Online: 0.2151, Phone: 0.4307, Total: 0.2296 },
    { period: "2025-06", year: 2025, month: "Jun", Online: 0.2116, Phone: 0.4177, Total: 0.2242 },
    { period: "2025-07", year: 2025, month: "Jul", Online: 0.207, Phone: 0.413, Total: 0.2224 },
    { period: "2025-08", year: 2025, month: "Aug", Online: 0.2049, Phone: 0.4064, Total: 0.2183 },
    { period: "2025-09", year: 2025, month: "Sep", Online: 0.2029, Phone: 0.3761, Total: 0.2143 },
    { period: "2025-10", year: 2025, month: "Oct", Online: 0.1836, Phone: 0.4013, Total: 0.2028 },
    { period: "2025-11", year: 2025, month: "Nov", Online: 0.1502, Phone: 0.2136, Total: 0.156 },
    { period: "2025-12", year: 2025, month: "Dec", Online: 0.106, Phone: 0.0105, Total: 0.0979 },
  ],
  gmvMonthly: [
    { period: "2024-01", year: 2024, month: "Jan", "Marketplace Retailers": 137145.49, "Coldwater Creek": 994795.55, Total: 1131941.04 },
    { period: "2024-02", year: 2024, month: "Feb", "Marketplace Retailers": 115724.34, "Coldwater Creek": 917301.42, Total: 1033025.76 },
    { period: "2024-03", year: 2024, month: "Mar", "Marketplace Retailers": 128672.9, "Coldwater Creek": 1082663.95, Total: 1211336.85 },
    { period: "2024-04", year: 2024, month: "Apr", "Marketplace Retailers": 125996.91, "Coldwater Creek": 1156367.72, Total: 1282364.63 },
    { period: "2024-05", year: 2024, month: "May", "Marketplace Retailers": 129846.31, "Coldwater Creek": 1264423.19, Total: 1394269.5 },
    { period: "2024-06", year: 2024, month: "Jun", "Marketplace Retailers": 128964.02, "Coldwater Creek": 1019434.59, Total: 1148398.61 },
    { period: "2024-07", year: 2024, month: "Jul", "Marketplace Retailers": 133893.16, "Coldwater Creek": 1136180.71, Total: 1270073.87 },
    { period: "2024-08", year: 2024, month: "Aug", "Marketplace Retailers": 136242.29, "Coldwater Creek": 1329824.37, Total: 1466066.66 },
    { period: "2024-09", year: 2024, month: "Sep", "Marketplace Retailers": 127438.7, "Coldwater Creek": 1311669.1, Total: 1439107.8 },
    { period: "2024-10", year: 2024, month: "Oct", "Marketplace Retailers": 142980.99, "Coldwater Creek": 1346035.62, Total: 1489016.61 },
    { period: "2024-11", year: 2024, month: "Nov", "Marketplace Retailers": 137471.06, "Coldwater Creek": 1477004.49, Total: 1614475.55 },
    { period: "2024-12", year: 2024, month: "Dec", "Marketplace Retailers": 116440.1, "Coldwater Creek": 1230315.36, Total: 1346755.46 },
    { period: "2025-01", year: 2025, month: "Jan", "Marketplace Retailers": 142764.04, "Coldwater Creek": 993362.05, Total: 1136126.09 },
    { period: "2025-02", year: 2025, month: "Feb", "Marketplace Retailers": 176117.2, "Coldwater Creek": 1048461.41, Total: 1224578.61 },
    { period: "2025-03", year: 2025, month: "Mar", "Marketplace Retailers": 175952.41, "Coldwater Creek": 1283227.14, Total: 1459179.55 },
    { period: "2025-04", year: 2025, month: "Apr", "Marketplace Retailers": 184905.16, "Coldwater Creek": 1311123.01, Total: 1496028.17 },
    { period: "2025-05", year: 2025, month: "May", "Marketplace Retailers": 172312.12, "Coldwater Creek": 2713594.46, Total: 2885906.58 },
    { period: "2025-06", year: 2025, month: "Jun", "Marketplace Retailers": 176363.82, "Coldwater Creek": 1363205.32, Total: 1539569.14 },
    { period: "2025-07", year: 2025, month: "Jul", "Marketplace Retailers": 162557.43, "Coldwater Creek": 1503938.71, Total: 1666496.14 },
    { period: "2025-08", year: 2025, month: "Aug", "Marketplace Retailers": 147574.56, "Coldwater Creek": 1612517.86, Total: 1760092.42 },
    { period: "2025-09", year: 2025, month: "Sep", "Marketplace Retailers": 146674.03, "Coldwater Creek": 1563258.7, Total: 1709932.73 },
    { period: "2025-10", year: 2025, month: "Oct", "Marketplace Retailers": 169124.96, "Coldwater Creek": 2152299.72, Total: 2321424.68 },
    { period: "2025-11", year: 2025, month: "Nov", "Marketplace Retailers": 183597.13, "Coldwater Creek": 2135421.26, Total: 2319018.39 },
    { period: "2025-12", year: 2025, month: "Dec", "Marketplace Retailers": 15929.21, "Coldwater Creek": 1142770.63, Total: 1158699.84 },
  ],
  claimsMonthly: [
    { period: "2024-01", year: 2024, month: "Jan", Online: 109139.41, Phone: 14126.73, Total: 123266.14 },
    { period: "2024-02", year: 2024, month: "Feb", Online: 100606.98, Phone: 10310.61, Total: 110917.59 },
    { period: "2024-03", year: 2024, month: "Mar", Online: 114991.62, Phone: 13556.69, Total: 128548.31 },
    { period: "2024-04", year: 2024, month: "Apr", Online: 126564.36, Phone: 14505.19, Total: 141069.55 },
    { period: "2024-05", year: 2024, month: "May", Online: 141952.78, Phone: 14694.49, Total: 156647.27 },
    { period: "2024-06", year: 2024, month: "Jun", Online: 124642.08, Phone: 12918.96, Total: 137561.04 },
    { period: "2024-07", year: 2024, month: "Jul", Online: 140392.12, Phone: 12360.99, Total: 152753.11 },
    { period: "2024-08", year: 2024, month: "Aug", Online: 152242.25, Phone: 13090.11, Total: 165332.36 },
    { period: "2024-09", year: 2024, month: "Sep", Online: 154387.91, Phone: 12622.17, Total: 167010.08 },
    { period: "2024-10", year: 2024, month: "Oct", Online: 169715.67, Phone: 15575.47, Total: 185291.14 },
    { period: "2024-11", year: 2024, month: "Nov", Online: 171243.12, Phone: 14347.66, Total: 185590.78 },
    { period: "2024-12", year: 2024, month: "Dec", Online: 143734.35, Phone: 14390.52, Total: 158124.87 },
    { period: "2025-01", year: 2025, month: "Jan", Online: 151719.98, Phone: 15307.73, Total: 167027.71 },
    { period: "2025-02", year: 2025, month: "Feb", Online: 163980.57, Phone: 15289.93, Total: 179270.5 },
    { period: "2025-03", year: 2025, month: "Mar", Online: 168932.74, Phone: 16569.24, Total: 185501.98 },
    { period: "2025-04", year: 2025, month: "Apr", Online: 181193.43, Phone: 16002.87, Total: 197196.3 },
    { period: "2025-05", year: 2025, month: "May", Online: 276696.12, Phone: 25192.69, Total: 301888.81 },
    { period: "2025-06", year: 2025, month: "Jun", Online: 185354.88, Phone: 15757.56, Total: 201112.44 },
    { period: "2025-07", year: 2025, month: "Jul", Online: 190727.63, Phone: 17012.28, Total: 207739.91 },
    { period: "2025-08", year: 2025, month: "Aug", Online: 171360.05, Phone: 15570.79, Total: 186930.84 },
    { period: "2025-09", year: 2025, month: "Sep", Online: 168122.72, Phone: 15061.27, Total: 183183.99 },
    { period: "2025-10", year: 2025, month: "Oct", Online: 226145.28, Phone: 21721.95, Total: 247867.23 },
    { period: "2025-11", year: 2025, month: "Nov", Online: 238632.02, Phone: 20301.26, Total: 258933.28 },
    { period: "2025-12", year: 2025, month: "Dec", Online: 106022.05, Phone: 10398.03, Total: 116420.08 },
  ],
  activeMonthly: [
    { date: "2024-01-01", Online: 1327857, Phone: 138868, Total: 1466725 },
    { date: "2024-02-01", Online: 1255356, Phone: 130532, Total: 1385888 },
    { date: "2024-03-01", Online: 1341300, Phone: 137554, Total: 1478854 },
    { date: "2024-04-01", Online: 1319012, Phone: 133531, Total: 1452543 },
    { date: "2024-05-01", Online: 1521814, Phone: 143912, Total: 1665726 },
    { date: "2024-06-01", Online: 1582688, Phone: 148510, Total: 1731198 },
    { date: "2024-07-01", Online: 1622223, Phone: 151086, Total: 1773309 },
    { date: "2024-08-01", Online: 1712064, Phone: 158404, Total: 1870468 },
    { date: "2024-09-01", Online: 1853977, Phone: 171245, Total: 2025222 },
    { date: "2024-10-01", Online: 2023459, Phone: 189074, Total: 2212533 },
    { date: "2024-11-01", Online: 2140196, Phone: 200246, Total: 2340442 },
    { date: "2024-12-01", Online: 2405561, Phone: 218228, Total: 2623789 },
    { date: "2025-01-01", Online: 2384638, Phone: 212236, Total: 2596874 },
    { date: "2025-02-01", Online: 2330395, Phone: 205328, Total: 2535723 },
    { date: "2025-03-01", Online: 2408259, Phone: 209799, Total: 2618058 },
    { date: "2025-04-01", Online: 2517812, Phone: 221587, Total: 2739399 },
    { date: "2025-05-01", Online: 2514703, Phone: 218316, Total: 2733019 },
    { date: "2025-06-01", Online: 2571107, Phone: 221265, Total: 2792372 },
    { date: "2025-07-01", Online: 2579628, Phone: 224292, Total: 2803920 },
    { date: "2025-08-01", Online: 2589418, Phone: 167676, Total: 2757094 },
    { date: "2025-09-01", Online: 2577429, Phone: 167518, Total: 2744947 },
    { date: "2025-10-01", Online: 2736629, Phone: 181817, Total: 2918446 },
    { date: "2025-11-01", Online: 2763667, Phone: 195046, Total: 2958713 },
    { date: "2025-12-01", Online: 863955, Phone: 62919, Total: 926874 },
  ],
  placementMonthly: [
    { period: "2024-01", year: 2024, month: "Jan", "Inflow Experience": 0.7784, Phone: 0.0766, "Order Confirmation - Bottom-Right": 0.145, "Order Confirmation - Top": 0.0, "Default Placement": 0.0 },
    { period: "2024-02", year: 2024, month: "Feb", "Inflow Experience": 0.7746, Phone: 0.0978, "Order Confirmation - Bottom-Right": 0.1276, "Order Confirmation - Top": 0.0, "Default Placement": 0.0 },
    { period: "2024-03", year: 2024, month: "Mar", "Inflow Experience": 0.7803, Phone: 0.0912, "Order Confirmation - Bottom-Right": 0.1283, "Order Confirmation - Top": 0.0, "Default Placement": 0.0 },
    { period: "2024-04", year: 2024, month: "Apr", "Inflow Experience": 0.78, Phone: 0.0876, "Order Confirmation - Bottom-Right": 0.105, "Order Confirmation - Top": 0.0273, "Default Placement": 0.0001 },
    { period: "2024-05", year: 2024, month: "May", "Inflow Experience": 0.782, Phone: 0.061, "Order Confirmation - Bottom-Right": 0.0803, "Order Confirmation - Top": 0.0767, "Default Placement": 0.0 },
    { period: "2024-06", year: 2024, month: "Jun", "Inflow Experience": 0.803, Phone: 0.0425, "Order Confirmation - Bottom-Right": 0.0643, "Order Confirmation - Top": 0.0902, "Default Placement": 0.0 },
    { period: "2024-07", year: 2024, month: "Jul", "Inflow Experience": 0.7945, Phone: 0.0484, "Order Confirmation - Bottom-Right": 0.0838, "Order Confirmation - Top": 0.0733, "Default Placement": 0.0 },
    { period: "2024-08", year: 2024, month: "Aug", "Inflow Experience": 0.797, Phone: 0.0543, "Order Confirmation - Bottom-Right": 0.091, "Order Confirmation - Top": 0.0577, "Default Placement": 0.0 },
    { period: "2024-09", year: 2024, month: "Sep", "Inflow Experience": 0.8227, Phone: 0.0598, "Order Confirmation - Bottom-Right": 0.0889, "Order Confirmation - Top": 0.0282, "Default Placement": 0.0002 },
    { period: "2024-10", year: 2024, month: "Oct", "Inflow Experience": 0.8095, Phone: 0.0752, "Order Confirmation - Bottom-Right": 0.0534, "Order Confirmation - Top": 0.0619, "Default Placement": 0.0 },
    { period: "2024-11", year: 2024, month: "Nov", "Inflow Experience": 0.841, Phone: 0.065, "Order Confirmation - Bottom-Right": 0.0178, "Order Confirmation - Top": 0.0762, "Default Placement": 0.0 },
    { period: "2024-12", year: 2024, month: "Dec", "Inflow Experience": 0.8542, Phone: 0.0774, "Order Confirmation - Bottom-Right": 0.0193, "Order Confirmation - Top": 0.0492, "Default Placement": 0.0 },
    { period: "2025-01", year: 2025, month: "Jan", "Inflow Experience": 0.883, Phone: 0.0831, "Order Confirmation - Bottom-Right": 0.018, "Order Confirmation - Top": 0.0159, "Default Placement": 0.0 },
    { period: "2025-02", year: 2025, month: "Feb", "Inflow Experience": 0.8489, Phone: 0.0827, "Order Confirmation - Bottom-Right": 0.035, "Order Confirmation - Top": 0.0332, "Default Placement": 0.0001 },
    { period: "2025-03", year: 2025, month: "Mar", "Inflow Experience": 0.8362, Phone: 0.0735, "Order Confirmation - Bottom-Right": 0.0456, "Order Confirmation - Top": 0.0443, "Default Placement": 0.0004 },
    { period: "2025-04", year: 2025, month: "Apr", "Inflow Experience": 0.8457, Phone: 0.0579, "Order Confirmation - Bottom-Right": 0.0481, "Order Confirmation - Top": 0.0484, "Default Placement": 0.0 },
    { period: "2025-05", year: 2025, month: "May", "Inflow Experience": 0.8816, Phone: 0.065, "Order Confirmation - Bottom-Right": 0.0282, "Order Confirmation - Top": 0.0251, "Default Placement": 0.0 },
    { period: "2025-06", year: 2025, month: "Jun", "Inflow Experience": 0.8914, Phone: 0.0621, "Order Confirmation - Bottom-Right": 0.0275, "Order Confirmation - Top": 0.0191, "Default Placement": 0.0 },
    { period: "2025-07", year: 2025, month: "Jul", "Inflow Experience": 0.8542, Phone: 0.0819, "Order Confirmation - Bottom-Right": 0.0332, "Order Confirmation - Top": 0.0308, "Default Placement": 0.0 },
    { period: "2025-08", year: 2025, month: "Aug", "Inflow Experience": 0.8738, Phone: 0.0666, "Order Confirmation - Bottom-Right": 0.0358, "Order Confirmation - Top": 0.0238, "Default Placement": 0.0 },
    { period: "2025-09", year: 2025, month: "Sep", "Inflow Experience": 0.8824, Phone: 0.0654, "Order Confirmation - Bottom-Right": 0.0303, "Order Confirmation - Top": 0.0218, "Default Placement": 0.0001 },
    { period: "2025-10", year: 2025, month: "Oct", "Inflow Experience": 0.8786, Phone: 0.0879, "Order Confirmation - Bottom-Right": 0.019, "Order Confirmation - Top": 0.0145, "Default Placement": 0.0 },
    { period: "2025-11", year: 2025, month: "Nov", "Inflow Experience": 0.8794, Phone: 0.0922, "Order Confirmation - Bottom-Right": 0.0166, "Order Confirmation - Top": 0.0118, "Default Placement": 0.0 },
    { period: "2025-12", year: 2025, month: "Dec", "Inflow Experience": 0.8884, Phone: 0.0843, "Order Confirmation - Bottom-Right": 0.0143, "Order Confirmation - Top": 0.0129, "Default Placement": 0.0 },
  ],
  funnelMonthly: [
    { period: "2024-01", year: 2024, month: "Jan", "Billable Members Cancel %": 0.86, "Cancels - billable members": 5235, "Net Members": 874, "Signups (to trial)": 7745, "Total Trial Cancel %": 0.21, "Trials converted to billables": 6109 },
    { period: "2024-02", year: 2024, month: "Feb", "Billable Members Cancel %": 0.85, "Cancels - billable members": 4672, "Net Members": 844, "Signups (to trial)": 7169, "Total Trial Cancel %": 0.23, "Trials converted to billables": 5516 },
    { period: "2024-03", year: 2024, month: "Mar", "Billable Members Cancel %": 0.84, "Cancels - billable members": 5100, "Net Members": 965, "Signups (to trial)": 7771, "Total Trial Cancel %": 0.22, "Trials converted to billables": 6065 },
    { period: "2024-04", year: 2024, month: "Apr", "Billable Members Cancel %": 0.84, "Cancels - billable members": 6736, "Net Members": 1302, "Signups (to trial)": 10334, "Total Trial Cancel %": 0.22, "Trials converted to billables": 8038 },
    { period: "2024-05", year: 2024, month: "May", "Billable Members Cancel %": 0.84, "Cancels - billable members": 9281, "Net Members": 1789, "Signups (to trial)": 14554, "Total Trial Cancel %": 0.24, "Trials converted to billables": 11070 },
    { period: "2024-06", year: 2024, month: "Jun", "Billable Members Cancel %": 0.81, "Cancels - billable members": 7784, "Net Members": 1456, "Signups (to trial)": 12692, "Total Trial Cancel %": 0.27, "Trials converted to billables": 9240 },
    { period: "2024-07", year: 2024, month: "Jul", "Billable Members Cancel %": 0.84, "Cancels - billable members": 6050, "Net Members": 1237, "Signups (to trial)": 9876, "Total Trial Cancel %": 0.26, "Trials converted to billables": 7287 },
    { period: "2024-08", year: 2024, month: "Aug", "Billable Members Cancel %": 0.83, "Cancels - billable members": 6395, "Net Members": 2098, "Signups (to trial)": 11094, "Total Trial Cancel %": 0.23, "Trials converted to billables": 8493 },
    { period: "2024-09", year: 2024, month: "Sep", "Billable Members Cancel %": 0.8, "Cancels - billable members": 6034, "Net Members": 3422, "Signups (to trial)": 12013, "Total Trial Cancel %": 0.21, "Trials converted to billables": 9456 },
    { period: "2024-10", year: 2024, month: "Oct", "Billable Members Cancel %": 0.78, "Cancels - billable members": 5992, "Net Members": 3495, "Signups (to trial)": 12964, "Total Trial Cancel %": 0.21, "Trials converted to billables": 11223 },
    { period: "2024-11", year: 2024, month: "Nov", "Billable Members Cancel %": 0.68, "Cancels - billable members": 6539, "Net Members": 5910, "Signups (to trial)": 18487, "Total Trial Cancel %": 0.2, "Trials converted to billables": 15175 },
    { period: "2024-12", year: 2024, month: "Dec", "Billable Members Cancel %": 0.58, "Cancels - billable members": 0, "Net Members": 13141, "Signups (to trial)": 13141, "Total Trial Cancel %": 0.2, "Trials converted to billables": 13141 },
    { period: "2025-01", year: 2025, month: "Jan", "Billable Members Cancel %": 0.55, "Cancels - billable members": 4726, "Net Members": 4421, "Signups (to trial)": 8855, "Total Trial Cancel %": 0.21, "Trials converted to billables": 9147 },
    { period: "2025-02", year: 2025, month: "Feb", "Billable Members Cancel %": 0.52, "Cancels - billable members": 3932, "Net Members": 4594, "Signups (to trial)": 10504, "Total Trial Cancel %": 0.22, "Trials converted to billables": 8526 },
    { period: "2025-03", year: 2025, month: "Mar", "Billable Members Cancel %": 0.46, "Cancels - billable members": 4020, "Net Members": 6319, "Signups (to trial)": 13592, "Total Trial Cancel %": 0.22, "Trials converted to billables": 10339 },
    { period: "2025-04", year: 2025, month: "Apr", "Billable Members Cancel %": 0.39, "Cancels - billable members": 3079, "Net Members": 8260, "Signups (to trial)": 17768, "Total Trial Cancel %": 0.21, "Trials converted to billables": 11339 },
    { period: "2025-05", year: 2025, month: "May", "Billable Members Cancel %": 0.27, "Cancels - billable members": 1617, "Net Members": 9635, "Signups (to trial)": 14209, "Total Trial Cancel %": 0.21, "Trials converted to billables": 11252 },
    { period: "2025-06", year: 2025, month: "Jun", "Billable Members Cancel %": 0.14, "Cancels - billable members": 274, "Net Members": 14901, "Signups (to trial)": 11582, "Total Trial Cancel %": 0.2, "Trials converted to billables": 15175 },
    { period: "2025-07", year: 2025, month: "Jul", "Billable Members Cancel %": 0.02, "Cancels - billable members": 0, "Net Members": 10957, "Signups (to trial)": 10957, "Total Trial Cancel %": 0.22, "Trials converted to billables": 10339 },
    { period: "2025-08", year: 2025, month: "Aug", "Billable Members Cancel %": 0.0, "Cancels - billable members": 0, "Net Members": 13227, "Signups (to trial)": 13227, "Total Trial Cancel %": 0.21, "Trials converted to billables": 11339 },
    { period: "2025-09", year: 2025, month: "Sep", "Billable Members Cancel %": 0.0, "Cancels - billable members": 0, "Net Members": 14431, "Signups (to trial)": 14431, "Total Trial Cancel %": 0.21, "Trials converted to billables": 11252 },
    { period: "2025-10", year: 2025, month: "Oct", "Billable Members Cancel %": 0.0, "Cancels - billable members": 0, "Net Members": 14114, "Signups (to trial)": 14114, "Total Trial Cancel %": 0.2, "Trials converted to billables": 15175 },
    { period: "2025-11", year: 2025, month: "Nov", "Billable Members Cancel %": 0.0, "Cancels - billable members": 0, "Net Members": 17980, "Signups (to trial)": 17980, "Total Trial Cancel %": 0.16, "Trials converted to billables": 15175 },
    { period: "2025-12", year: 2025, month: "Dec", "Billable Members Cancel %": 0.0, "Cancels - billable members": 0, "Net Members": 5093, "Signups (to trial)": 5646, "Total Trial Cancel %": 0.1, "Trials converted to billables": 5093 },
  ],
  kpis: {
    joins: { "2024": 137840, "2025": 152865, yoy: 0.109, grand_total_2024_2025: 290705 },
    online_share: { "2024": 0.9323, "2025": 0.9256 },
    trial_cancel_total: { "2024": 0.2212, "2025": 0.2049 },
    gmv: { "2024": 16001503.84, "2025": 20521640.03, yoy: 0.2825 },
    claims: { "2024": 1737175.64, "2025": 2184977.62, yoy: 0.2576 },
    gmv_per_join: { "2024": 116.09, "2025": 134.25 },
    claims_per_join: { "2024": 12.6, "2025": 14.29 },
    claim_detail: {
      avg_claim: { "2024": 45.58, "2025": 47.66 },
      claim_count: { "2024": 38110, "2025": 45844 },
      distinct_members: { "2024": 61993, "2025": 65663 },
    },
    active_peak: { date: "2025-11-01", total: 2958713 },
    peaks: {
      joins: {
        "2024": { month: "Nov", Total: 18487, period: "2024-11" },
        "2025": { month: "Nov", Total: 17980, period: "2025-11" },
      },
      gmv: {
        "2024": { month: "Nov", Total: 1614475.55, period: "2024-11" },
        "2025": { month: "May", Total: 2885906.58, period: "2025-05" },
      },
      claims: {
        "2024": { month: "Nov", Total: 185590.78, period: "2024-11" },
        "2025": { month: "May", Total: 301888.81, period: "2025-05" },
      },
    },
    funnel_totals_all: {
      "Signups (to trial)": 290705,
      "Total Trial Cancel Count": 61818,
      "Total Trial Cancel %": 0.21,
      "Trials converted to billables": 228887,
      "Cancels - billable members": 134316,
      "Billable Members Cancel %": 0.59,
      "Net Members": 94571,
    },
  },
};

// Okabe–Ito (colorblind-friendly) palette
const COLORS = {
  blue: "#0072B2",
  sky: "#56B4E9",
  green: "#009E73",
  orange: "#E69F00",
  vermillion: "#D55E00",
  purple: "#CC79A7",
  gray: "#4B5563",
};

const fmtInt = new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 });
const fmtMoney = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" });
const fmtPct = new Intl.NumberFormat("en-US", { style: "percent", maximumFractionDigits: 1 });

// --- Minimal “test cases” (sanity assertions) ---
// We don't have a full test runner in this single-file canvas, so we do lightweight runtime checks.
const __TESTS__ = (() => {
  const assert = (cond: any, msg: string) => {
    if (!cond) console.warn(`[Dashboard sanity check failed] ${msg}`);
  };

  assert(Array.isArray(DATA.joinsMonthly) && DATA.joinsMonthly.length > 0, "joinsMonthly should be non-empty");
  assert(Array.isArray(DATA.gmvMonthly) && DATA.gmvMonthly.length > 0, "gmvMonthly should be non-empty");
  assert(typeof DATA.kpis?.joins?.["2025"] === "number" && DATA.kpis.joins["2025"] > 0, "kpis.joins[2025] should exist");
  assert(
    typeof DATA.kpis?.trial_cancel_total?.["2025"] === "number" && DATA.kpis.trial_cancel_total["2025"] > 0,
    "kpis.trial_cancel_total[2025] should exist"
  );

  return true;
})();

function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null;
  return (
    <div className="rounded-2xl border bg-white p-3 shadow-sm">
      <div className="text-sm font-semibold">{label}</div>
      <div className="mt-2 space-y-1">
        {payload.map((p: any) => (
          <div key={p.dataKey} className="flex items-center justify-between gap-6 text-sm">
            <span className="text-slate-600">{p.name}</span>
            <span className="font-medium">
              {typeof p.value === "number" ? p.value.toLocaleString() : String(p.value)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

function KpiCard({ title, value, sub, badge }: any) {
  return (
    <Card className="rounded-2xl shadow-sm">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-slate-600">{title}</CardTitle>
      </CardHeader>
      <CardContent className="pt-0">
        <div className="flex items-baseline justify-between gap-3">
          <div className="text-2xl font-semibold">{value}</div>
          {badge ? (
            <Badge variant="secondary" className="rounded-xl">
              {badge}
            </Badge>
          ) : null}
        </div>
        {sub ? <div className="mt-1 text-xs text-slate-600">{sub}</div> : null}
      </CardContent>
    </Card>
  );
}

export default function Dashboard() {
  const [year, setYear] = useState("All");
  const yearNum = year === "All" ? null : Number(year);

  const joins = useMemo(
    () => (yearNum ? DATA.joinsMonthly.filter((d: any) => d.year === yearNum) : DATA.joinsMonthly),
    [yearNum]
  );
  const trial = useMemo(
    () => (yearNum ? DATA.trialCancelMonthly.filter((d: any) => d.year === yearNum) : DATA.trialCancelMonthly),
    [yearNum]
  );
  const gmv = useMemo(
    () => (yearNum ? DATA.gmvMonthly.filter((d: any) => d.year === yearNum) : DATA.gmvMonthly),
    [yearNum]
  );
  const claims = useMemo(
    () => (yearNum ? DATA.claimsMonthly.filter((d: any) => d.year === yearNum) : DATA.claimsMonthly),
    [yearNum]
  );
  const placement = useMemo(
    () => (yearNum ? DATA.placementMonthly.filter((d: any) => d.year === yearNum) : DATA.placementMonthly),
    [yearNum]
  );

  // Active members is date-based (2024-01..2025-12). If a year is selected, filter.
  const active = useMemo(() => {
    if (!yearNum) return DATA.activeMonthly;
    return DATA.activeMonthly.filter((d: any) => d.date.startsWith(String(yearNum)));
  }, [yearNum]);

  const dec2025LooksPartial = useMemo(() => {
    const nov = DATA.activeMonthly.find((d: any) => d.date === "2025-11-01")?.Total ?? null;
    const dec = DATA.activeMonthly.find((d: any) => d.date === "2025-12-01")?.Total ?? null;
    if (!nov || !dec) return false;
    return dec < nov * 0.6;
  }, []);

  const k: any = DATA.kpis;
  const yoyBadge = (x: any) => (typeof x === "number" ? `${fmtPct.format(x)} YoY` : "—");

  // Derived “so what” metrics for the Opportunities section
  const gmvPerJoinLift = k.gmv_per_join["2025"] / k.gmv_per_join["2024"] - 1;
  const claimsPerJoinLift = k.claims_per_join["2025"] / k.claims_per_join["2024"] - 1;
  const avgClaimLift = k.claim_detail.avg_claim["2025"] / k.claim_detail.avg_claim["2024"] - 1;

  const trialPpChange = (k.trial_cancel_total["2025"] - k.trial_cancel_total["2024"]) * 100; // percentage points
  const estExtraConversionsPerPp = Math.round(k.joins["2025"] * 0.01);

  const avgTrial = (yr: number, key: "Online" | "Phone" | "Total", { excludePeriods = [] as string[] } = {}) => {
    const rows = DATA.trialCancelMonthly.filter(
      (d: any) => d.year === yr && !excludePeriods.includes(d.period)
    );
    const denom = rows.length || 1;
    return rows.reduce((s: number, d: any) => s + (d[key] ?? 0), 0) / denom;
  };

  // Dec 2025 looks incomplete across series; exclude for cleaner signal
  const trial2025Online = avgTrial(2025, "Online", { excludePeriods: ["2025-12"] });
  const trial2025Phone = avgTrial(2025, "Phone", { excludePeriods: ["2025-12"] });

  return (
    <div className="min-h-screen bg-slate-50 p-4 md:p-8">
      <div className="mx-auto max-w-7xl space-y-6">
        <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
          <div>
            <div className="text-3xl font-semibold tracking-tight">Coldwater Creek • 2024–2025 Dashboard</div>
            <div className="mt-1 text-sm text-slate-600">
              Built from your uploaded Year-in-Review workbook (Sheet 1). Toggle year to focus on 2024 or 2025.
            </div>
          </div>
          <div className="w-full md:w-[240px]">
            <Select value={year} onValueChange={setYear}>
              <SelectTrigger className="rounded-2xl bg-white">
                <SelectValue placeholder="Select year" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="All">All (2024–2025)</SelectItem>
                <SelectItem value="2024">2024</SelectItem>
                <SelectItem value="2025">2025</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        <Tabs defaultValue="overview" className="w-full">
          <TabsList className="grid w-full grid-cols-2 md:grid-cols-5 rounded-2xl bg-white">
            <TabsTrigger value="overview" className="rounded-2xl">
              Overview
            </TabsTrigger>
            <TabsTrigger value="acq" className="rounded-2xl">
              Acquisition & Trials
            </TabsTrigger>
            <TabsTrigger value="members" className="rounded-2xl">
              Members
            </TabsTrigger>
            <TabsTrigger value="revenue" className="rounded-2xl">
              Revenue & Claims
            </TabsTrigger>
            <TabsTrigger value="placement" className="rounded-2xl">
              Placement Mix
            </TabsTrigger>
          </TabsList>

          <TabsContent value="overview">
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              <div className="grid grid-cols-1 gap-3 md:grid-cols-4">
                <KpiCard
                  title="Joins (2025)"
                  value={fmtInt.format(k.joins["2025"])}
                  sub={`2024: ${fmtInt.format(k.joins["2024"])}`}
                  badge={yoyBadge(k.joins.yoy)}
                />
                <KpiCard
                  title="Total GMV (2025)"
                  value={fmtMoney.format(k.gmv["2025"])}
                  sub={`2024: ${fmtMoney.format(k.gmv["2024"])}`}
                  badge={yoyBadge(k.gmv.yoy)}
                />
                <KpiCard
                  title="Claims $ (2025)"
                  value={fmtMoney.format(k.claims["2025"])}
                  sub={`2024: ${fmtMoney.format(k.claims["2024"])}`}
                  badge={yoyBadge(k.claims.yoy)}
                />
                <KpiCard
                  title="Trial Cancel % (Total)"
                  value={fmtPct.format(k.trial_cancel_total["2025"])}
                  sub={`2024: ${fmtPct.format(k.trial_cancel_total["2024"])}`}
                  badge={k.trial_cancel_total["2025"] < k.trial_cancel_total["2024"] ? "Improving" : "Worsening"}
                />
              </div>

              <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
                <Card className="rounded-2xl shadow-sm">
                  <CardHeader>
                    <CardTitle>Monthly Joins (Online vs Phone)</CardTitle>
                  </CardHeader>
                  <CardContent className="h-[360px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={joins} margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="period" tick={{ fontSize: 12 }} />
                        <YAxis tick={{ fontSize: 12 }} />
                        <Tooltip content={<CustomTooltip />} />
                        <Legend />
                        <Bar dataKey="Online" stackId="a" fill={COLORS.blue} />
                        <Bar dataKey="Phone" stackId="a" fill={COLORS.orange} />
                        <Line type="monotone" dataKey="Total" stroke={COLORS.green} strokeWidth={2} dot={false} />
                      </BarChart>
                    </ResponsiveContainer>
                    <div className="mt-3 text-xs text-slate-600">
                      Peak joins month: 2024 {k.peaks.joins["2024"].month} ({fmtInt.format(k.peaks.joins["2024"].Total)}), 2025 {k.peaks.joins["2025"].month} ({fmtInt.format(k.peaks.joins["2025"].Total)})
                    </div>
                  </CardContent>
                </Card>

                <Card className="rounded-2xl shadow-sm">
                  <CardHeader>
                    <CardTitle>GMV Trend</CardTitle>
                  </CardHeader>
                  <CardContent className="h-[360px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={gmv} margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="period" tick={{ fontSize: 12 }} />
                        <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `$${(Number(v) / 1_000_000).toFixed(1)}M`} />
                        <Tooltip
                          content={({ active, payload, label }: any) => {
                            if (!active || !payload?.length) return null;
                            const byKey = Object.fromEntries(payload.map((p: any) => [p.dataKey, p.value]));
                            return (
                              <div className="rounded-2xl border bg-white p-3 shadow-sm">
                                <div className="text-sm font-semibold">{label}</div>
                                <div className="mt-2 space-y-1 text-sm">
                                  <div className="flex justify-between gap-6">
                                    <span className="text-slate-600">Total</span>
                                    <span className="font-medium">{fmtMoney.format(byKey.Total ?? 0)}</span>
                                  </div>
                                  <div className="flex justify-between gap-6">
                                    <span className="text-slate-600">Coldwater Creek</span>
                                    <span className="font-medium">{fmtMoney.format(byKey["Coldwater Creek"] ?? 0)}</span>
                                  </div>
                                  <div className="flex justify-between gap-6">
                                    <span className="text-slate-600">Marketplace Retailers</span>
                                    <span className="font-medium">{fmtMoney.format(byKey["Marketplace Retailers"] ?? 0)}</span>
                                  </div>
                                </div>
                              </div>
                            );
                          }}
                        />
                        <Legend />
                        <Line type="monotone" dataKey="Total" stroke={COLORS.green} strokeWidth={2} dot={false} />
                        <Line type="monotone" dataKey="Coldwater Creek" stroke={COLORS.blue} dot={false} />
                        <Line type="monotone" dataKey="Marketplace Retailers" stroke={COLORS.orange} dot={false} />
                      </LineChart>
                    </ResponsiveContainer>
                    <div className="mt-3 text-xs text-slate-600">
                      GMV per join: 2024 {fmtMoney.format(k.gmv_per_join["2024"])}, 2025 {fmtMoney.format(k.gmv_per_join["2025"])}
                    </div>
                  </CardContent>
                </Card>
              </div>

              <Card className="rounded-2xl shadow-sm">
                <CardHeader>
                  <CardTitle>Claims Trend</CardTitle>
                </CardHeader>
                <CardContent className="h-[320px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={claims} margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="period" tick={{ fontSize: 12 }} />
                      <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `$${(Number(v) / 1000).toFixed(0)}k`} />
                      <Tooltip
                        content={({ active, payload, label }: any) => {
                          if (!active || !payload?.length) return null;
                          const byKey = Object.fromEntries(payload.map((p: any) => [p.dataKey, p.value]));
                          return (
                            <div className="rounded-2xl border bg-white p-3 shadow-sm">
                              <div className="text-sm font-semibold">{label}</div>
                              <div className="mt-2 space-y-1 text-sm">
                                <div className="flex justify-between gap-6">
                                  <span className="text-slate-600">Total</span>
                                  <span className="font-medium">{fmtMoney.format(byKey.Total ?? 0)}</span>
                                </div>
                                <div className="flex justify-between gap-6">
                                  <span className="text-slate-600">Online</span>
                                  <span className="font-medium">{fmtMoney.format(byKey.Online ?? 0)}</span>
                                </div>
                                <div className="flex justify-between gap-6">
                                  <span className="text-slate-600">Phone</span>
                                  <span className="font-medium">{fmtMoney.format(byKey.Phone ?? 0)}</span>
                                </div>
                              </div>
                            </div>
                          );
                        }}
                      />
                      <Legend />
                      <Line type="monotone" dataKey="Total" stroke={COLORS.vermillion} strokeWidth={2} dot={false} />
                      <Line type="monotone" dataKey="Online" stroke={COLORS.blue} dot={false} />
                      <Line type="monotone" dataKey="Phone" stroke={COLORS.orange} dot={false} />
                    </LineChart>
                  </ResponsiveContainer>
                  <div className="mt-3 text-xs text-slate-600">
                    Avg claim amount (Total): 2024 {fmtMoney.format(k.claim_detail.avg_claim["2024"])}, 2025 {fmtMoney.format(k.claim_detail.avg_claim["2025"])}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </TabsContent>

          <TabsContent value="acq">
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
                <Card className="rounded-2xl shadow-sm">
                  <CardHeader>
                    <CardTitle>Trial Cancel % (Online vs Phone)</CardTitle>
                  </CardHeader>
                  <CardContent className="h-[360px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={trial} margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="period" tick={{ fontSize: 12 }} />
                        <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `${Math.round(Number(v) * 100)}%`} />
                        <Tooltip
                          content={({ active, payload, label }: any) => {
                            if (!active || !payload?.length) return null;
                            const byKey = Object.fromEntries(payload.map((p: any) => [p.dataKey, p.value]));
                            return (
                              <div className="rounded-2xl border bg-white p-3 shadow-sm">
                                <div className="text-sm font-semibold">{label}</div>
                                <div className="mt-2 space-y-1 text-sm">
                                  <div className="flex justify-between gap-6">
                                    <span className="text-slate-600">Total</span>
                                    <span className="font-medium">{fmtPct.format(byKey.Total ?? 0)}</span>
                                  </div>
                                  <div className="flex justify-between gap-6">
                                    <span className="text-slate-600">Online</span>
                                    <span className="font-medium">{fmtPct.format(byKey.Online ?? 0)}</span>
                                  </div>
                                  <div className="flex justify-between gap-6">
                                    <span className="text-slate-600">Phone</span>
                                    <span className="font-medium">{fmtPct.format(byKey.Phone ?? 0)}</span>
                                  </div>
                                </div>
                              </div>
                            );
                          }}
                        />
                        <Legend />
                        <Line type="monotone" dataKey="Total" stroke={COLORS.green} strokeWidth={2} dot={false} />
                        <Line type="monotone" dataKey="Online" stroke={COLORS.blue} dot={false} />
                        <Line type="monotone" dataKey="Phone" stroke={COLORS.orange} dot={false} />
                      </LineChart>
                    </ResponsiveContainer>
                    <div className="mt-3 text-xs text-slate-600">
                      2025 total trial cancel: {fmtPct.format(k.trial_cancel_total["2025"])} (vs {fmtPct.format(k.trial_cancel_total["2024"])} in 2024)
                    </div>
                  </CardContent>
                </Card>

                <Card className="rounded-2xl shadow-sm">
                  <CardHeader>
                    <CardTitle>Joins → Net Members (from Funnel Block)</CardTitle>
                  </CardHeader>
                  <CardContent className="h-[360px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart
                        data={DATA.funnelMonthly.filter((d: any) => (yearNum ? d.year === yearNum : true))}
                        margin={{ top: 10, right: 20, bottom: 10, left: 0 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="period" tick={{ fontSize: 12 }} />
                        <YAxis tick={{ fontSize: 12 }} />
                        <Tooltip
                          content={({ active, payload, label }: any) => {
                            if (!active || !payload?.length) return null;
                            const byKey = Object.fromEntries(payload.map((p: any) => [p.dataKey, p.value]));
                            return (
                              <div className="rounded-2xl border bg-white p-3 shadow-sm">
                                <div className="text-sm font-semibold">{label}</div>
                                <div className="mt-2 space-y-1 text-sm">
                                  <div className="flex justify-between gap-6">
                                    <span className="text-slate-600">Signups</span>
                                    <span className="font-medium">{fmtInt.format(byKey["Signups (to trial)"] ?? 0)}</span>
                                  </div>
                                  <div className="flex justify-between gap-6">
                                    <span className="text-slate-600">Net Members</span>
                                    <span className="font-medium">{fmtInt.format(byKey["Net Members"] ?? 0)}</span>
                                  </div>
                                  <Separator className="my-2" />
                                  <div className="flex justify-between gap-6">
                                    <span className="text-slate-600">Trial Cancel %</span>
                                    <span className="font-medium">{fmtPct.format(byKey["Total Trial Cancel %"] ?? 0)}</span>
                                  </div>
                                  <div className="flex justify-between gap-6">
                                    <span className="text-slate-600">Billable Cancel %</span>
                                    <span className="font-medium">{fmtPct.format(byKey["Billable Members Cancel %"] ?? 0)}</span>
                                  </div>
                                </div>
                              </div>
                            );
                          }}
                        />
                        <Legend />
                        <Bar dataKey="Signups (to trial)" fill={COLORS.sky} />
                        <Bar dataKey="Net Members" fill={COLORS.green} />
                      </BarChart>
                    </ResponsiveContainer>
                    <div className="mt-3 text-xs text-slate-600">
                      Totals (2024–2025): {fmtInt.format(k.funnel_totals_all["Signups (to trial)"])} signups → {fmtInt.format(k.funnel_totals_all["Net Members"])} net members.
                    </div>
                  </CardContent>
                </Card>
              </div>

              <Card className="rounded-2xl shadow-sm">
                <CardHeader>
                  <CardTitle>External Benchmarks (Context Only)</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3 text-sm text-slate-700">
                  <div className="rounded-2xl border bg-white p-3">
                    <div className="font-semibold">Trial cancellations vary heavily by trial length</div>
                    <div className="mt-1 text-slate-600">
                      Recent benchmark summaries based on RevenueCat: ~26% cancellations for ~3-day trials vs ~51% for ~30-day trials (apps context).
                    </div>
                  </div>
                  <div className="rounded-2xl border bg-white p-3">
                    <div className="font-semibold">Retention-first trend</div>
                    <div className="mt-1 text-slate-600">
                      Recurly’s 2025 State of Subscriptions highlights the shift toward retention as acquisition slows; pause features are cited as a high-impact retention lever.
                    </div>
                  </div>
                  <div className="text-xs text-slate-500">These cards are for directional comparison only and are not used in any calculations above.</div>
                </CardContent>
              </Card>
            </motion.div>
          </TabsContent>

          <TabsContent value="members">
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              <Card className="rounded-2xl shadow-sm">
                <CardHeader>
                  <CardTitle>Active Members (Online / Phone / Total)</CardTitle>
                </CardHeader>
                <CardContent className="h-[380px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={active} margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" tick={{ fontSize: 12 }} />
                      <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `${(Number(v) / 1_000_000).toFixed(1)}M`} />
                      <Tooltip
                        content={({ active, payload, label }: any) => {
                          if (!active || !payload?.length) return null;
                          const byKey = Object.fromEntries(payload.map((p: any) => [p.dataKey, p.value]));
                          return (
                            <div className="rounded-2xl border bg-white p-3 shadow-sm">
                              <div className="text-sm font-semibold">{label}</div>
                              <div className="mt-2 space-y-1 text-sm">
                                <div className="flex justify-between gap-6">
                                  <span className="text-slate-600">Total</span>
                                  <span className="font-medium">{fmtInt.format(byKey.Total ?? 0)}</span>
                                </div>
                                <div className="flex justify-between gap-6">
                                  <span className="text-slate-600">Online</span>
                                  <span className="font-medium">{fmtInt.format(byKey.Online ?? 0)}</span>
                                </div>
                                <div className="flex justify-between gap-6">
                                  <span className="text-slate-600">Phone</span>
                                  <span className="font-medium">{fmtInt.format(byKey.Phone ?? 0)}</span>
                                </div>
                              </div>
                            </div>
                          );
                        }}
                      />
                      <Legend />
                      <Line type="monotone" dataKey="Total" stroke={COLORS.green} strokeWidth={2} dot={false} />
                      <Line type="monotone" dataKey="Online" stroke={COLORS.blue} dot={false} />
                      <Line type="monotone" dataKey="Phone" stroke={COLORS.orange} dot={false} />
                    </LineChart>
                  </ResponsiveContainer>
                  <div className="mt-3 text-xs text-slate-600">
                    Peak active total: {k.active_peak.date} ({fmtInt.format(k.active_peak.total)}).{" "}
                    {dec2025LooksPartial
                      ? "Note: Dec 2025 appears unusually low vs Nov 2025 (may be partial / reporting cut-off)."
                      : ""}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </TabsContent>

          <TabsContent value="revenue">
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
                <Card className="rounded-2xl shadow-sm">
                  <CardHeader>
                    <CardTitle>GMV Breakdown</CardTitle>
                  </CardHeader>
                  <CardContent className="h-[360px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={gmv} margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="period" tick={{ fontSize: 12 }} />
                        <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `$${(Number(v) / 1_000_000).toFixed(1)}M`} />
                        <Tooltip
                          content={({ active, payload, label }: any) => {
                            if (!active || !payload?.length) return null;
                            const byKey = Object.fromEntries(payload.map((p: any) => [p.dataKey, p.value]));
                            return (
                              <div className="rounded-2xl border bg-white p-3 shadow-sm">
                                <div className="text-sm font-semibold">{label}</div>
                                <div className="mt-2 space-y-1 text-sm">
                                  <div className="flex justify-between gap-6">
                                    <span className="text-slate-600">Coldwater Creek</span>
                                    <span className="font-medium">{fmtMoney.format(byKey["Coldwater Creek"] ?? 0)}</span>
                                  </div>
                                  <div className="flex justify-between gap-6">
                                    <span className="text-slate-600">Marketplace</span>
                                    <span className="font-medium">{fmtMoney.format(byKey["Marketplace Retailers"] ?? 0)}</span>
                                  </div>
                                  <Separator className="my-2" />
                                  <div className="flex justify-between gap-6">
                                    <span className="text-slate-600">Total</span>
                                    <span className="font-medium">{fmtMoney.format(byKey.Total ?? 0)}</span>
                                  </div>
                                </div>
                              </div>
                            );
                          }}
                        />
                        <Legend />
                        <Area type="monotone" dataKey="Coldwater Creek" stackId="a" stroke={COLORS.blue} fill={COLORS.blue} fillOpacity={0.18} />
                        <Area type="monotone" dataKey="Marketplace Retailers" stackId="a" stroke={COLORS.orange} fill={COLORS.orange} fillOpacity={0.18} />
                      </AreaChart>
                    </ResponsiveContainer>
                    <div className="mt-3 text-xs text-slate-600">
                      Peak GMV month: 2025 {k.peaks.gmv["2025"].month} ({fmtMoney.format(k.peaks.gmv["2025"].Total)})
                    </div>
                  </CardContent>
                </Card>

                <Card className="rounded-2xl shadow-sm">
                  <CardHeader>
                    <CardTitle>Claims Breakdown</CardTitle>
                  </CardHeader>
                  <CardContent className="h-[360px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={claims} margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="period" tick={{ fontSize: 12 }} />
                        <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `$${(Number(v) / 1000).toFixed(0)}k`} />
                        <Tooltip
                          content={({ active, payload, label }: any) => {
                            if (!active || !payload?.length) return null;
                            const byKey = Object.fromEntries(payload.map((p: any) => [p.dataKey, p.value]));
                            return (
                              <div className="rounded-2xl border bg-white p-3 shadow-sm">
                                <div className="text-sm font-semibold">{label}</div>
                                <div className="mt-2 space-y-1 text-sm">
                                  <div className="flex justify-between gap-6">
                                    <span className="text-slate-600">Online</span>
                                    <span className="font-medium">{fmtMoney.format(byKey.Online ?? 0)}</span>
                                  </div>
                                  <div className="flex justify-between gap-6">
                                    <span className="text-slate-600">Phone</span>
                                    <span className="font-medium">{fmtMoney.format(byKey.Phone ?? 0)}</span>
                                  </div>
                                  <Separator className="my-2" />
                                  <div className="flex justify-between gap-6">
                                    <span className="text-slate-600">Total</span>
                                    <span className="font-medium">{fmtMoney.format(byKey.Total ?? 0)}</span>
                                  </div>
                                </div>
                              </div>
                            );
                          }}
                        />
                        <Legend />
                        <Area type="monotone" dataKey="Online" stackId="b" stroke={COLORS.blue} fill={COLORS.blue} fillOpacity={0.18} />
                        <Area type="monotone" dataKey="Phone" stackId="b" stroke={COLORS.orange} fill={COLORS.orange} fillOpacity={0.18} />
                      </AreaChart>
                    </ResponsiveContainer>
                    <div className="mt-3 text-xs text-slate-600">
                      Claims per join: 2024 {fmtMoney.format(k.claims_per_join["2024"])}, 2025 {fmtMoney.format(k.claims_per_join["2025"]) }
                    </div>
                  </CardContent>
                </Card>
              </div>
            </motion.div>
          </TabsContent>

          <TabsContent value="placement">
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              <Card className="rounded-2xl shadow-sm">
                <CardHeader>
                  <CardTitle>Join Placement Mix (Top 5 by 2025 Avg Share)</CardTitle>
                </CardHeader>
                <CardContent className="h-[380px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={placement} margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="period" tick={{ fontSize: 12 }} />
                      <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `${Math.round(Number(v) * 100)}%`} />
                      <Tooltip
                        content={({ active, payload, label }: any) => {
                          if (!active || !payload?.length) return null;
                          return (
                            <div className="rounded-2xl border bg-white p-3 shadow-sm">
                              <div className="text-sm font-semibold">{label}</div>
                              <div className="mt-2 space-y-1 text-sm">
                                {payload
                                  .slice()
                                  .sort((a: any, b: any) => (b.value ?? 0) - (a.value ?? 0))
                                  .map((p: any) => (
                                    <div key={p.dataKey} className="flex justify-between gap-6">
                                      <span className="text-slate-600">{p.name}</span>
                                      <span className="font-medium">{fmtPct.format(p.value ?? 0)}</span>
                                    </div>
                                  ))}
                              </div>
                            </div>
                          );
                        }}
                      />
                      <Legend />
                      <Area type="monotone" dataKey="Inflow Experience" stackId="p" stroke={COLORS.green} fill={COLORS.green} fillOpacity={0.18} />
                      <Area type="monotone" dataKey="Phone" stackId="p" stroke={COLORS.orange} fill={COLORS.orange} fillOpacity={0.18} />
                      <Area type="monotone" dataKey="Order Confirmation - Bottom-Right" stackId="p" stroke={COLORS.blue} fill={COLORS.blue} fillOpacity={0.18} />
                      <Area type="monotone" dataKey="Order Confirmation - Top" stackId="p" stroke={COLORS.purple} fill={COLORS.purple} fillOpacity={0.18} />
                      <Area type="monotone" dataKey="Default Placement" stackId="p" stroke={COLORS.gray} fill={COLORS.gray} fillOpacity={0.18} />
                    </AreaChart>
                  </ResponsiveContainer>
                  <div className="mt-3 text-xs text-slate-600">
                    Inflow Experience dominates the join placement mix (avg share ~87% in 2025 in your data), with Phone and Order Confirmation placements contributing the remainder.
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </TabsContent>
        </Tabs>

        {/* Opportunities & Analysis */}
        <div className="rounded-2xl border bg-white p-4 shadow-sm">
          <div className="flex flex-col gap-2 md:flex-row md:items-start md:justify-between">
            <div>
              <div className="text-base font-semibold">Opportunities &amp; Analysis (Internal)</div>
              <div className="mt-1 text-sm text-slate-600">
                Ranked by Impact × Confidence. Translation: where the data already screams and we can actually pull a lever.
              </div>
            </div>
            <div className="flex flex-wrap gap-2">
              <Badge variant="secondary" className="rounded-xl">2025 vs 2024</Badge>
              <Badge variant="secondary" className="rounded-xl">{fmtPct.format(k.gmv.yoy)} GMV YoY</Badge>
              <Badge variant="secondary" className="rounded-xl">{fmtPct.format(k.joins.yoy)} Joins YoY</Badge>
            </div>
          </div>

          <Separator className="my-4" />

          <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
            <div className="rounded-2xl border bg-slate-50 p-3">
              <div className="font-semibold">What’s working (keep doing it, but louder)</div>
              <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-700">
                <li>
                  <span className="font-medium">Revenue efficiency improved:</span> GMV per join is {fmtMoney.format(k.gmv_per_join["2025"])} in 2025 vs {fmtMoney.format(k.gmv_per_join["2024"])} in 2024 ({fmtPct.format(gmvPerJoinLift)}).
                </li>
                <li>
                  <span className="font-medium">Claims scale with growth:</span> claims $ is up {fmtPct.format(k.claims.yoy)} YoY; claims per join rose to {fmtMoney.format(k.claims_per_join["2025"])} ({fmtPct.format(claimsPerJoinLift)}).
                </li>
                <li>
                  <span className="font-medium">Trial cancels improved:</span> total trial cancel is {fmtPct.format(k.trial_cancel_total["2025"])} vs {fmtPct.format(k.trial_cancel_total["2024"])} ({trialPpChange < 0 ? `${Math.abs(trialPpChange).toFixed(1)}pp better` : `${trialPpChange.toFixed(1)}pp worse`} ).
                </li>
                <li>
                  <span className="font-medium">Value per claim nudged up:</span> avg claim is {fmtMoney.format(k.claim_detail.avg_claim["2025"])} in 2025 vs {fmtMoney.format(k.claim_detail.avg_claim["2024"])} in 2024 ({fmtPct.format(avgClaimLift)}).
                </li>
              </ul>
            </div>

            <div className="rounded-2xl border bg-slate-50 p-3">
              <div className="font-semibold">Where to dig in (aka the expensive weirdness)</div>
              <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-700">
                <li>
                  <span className="font-medium">Phone trial cancels are much higher:</span> ~{fmtPct.format(trial2025Phone)} (phone) vs ~{fmtPct.format(trial2025Online)} (online) in 2025 (excluding Dec).
                </li>
                <li>
                  <span className="font-medium">May 2025 is a monster month:</span> peak GMV {fmtMoney.format(k.peaks.gmv["2025"].Total)} and peak claims {fmtMoney.format(k.peaks.claims["2025"].Total)} — likely promo / assortment / reporting behavior worth explaining.
                </li>
                <li>
                  <span className="font-medium">Dec 2025 likely partial:</span> multiple series dip unusually vs Nov; treat MoM comparisons carefully.
                </li>
              </ul>
            </div>
          </div>

          <div className="mt-4">
            <div className="flex flex-col gap-1 md:flex-row md:items-end md:justify-between">
              <div className="text-sm font-semibold">Ranked opportunities (Impact × Confidence)</div>
              <div className="text-xs text-slate-600">Internal: focus on controllable levers; leave the “maybe data is wrong” stuff for validation work.</div>
            </div>

            <div className="mt-3 grid grid-cols-1 gap-3 md:grid-cols-3">
              <div className="rounded-2xl border p-3">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <div className="font-semibold">1) Fix phone trial cancels</div>
                    <div className="mt-0.5 text-xs text-slate-600">Big gap + clean lever.</div>
                  </div>
                  <div className="flex flex-col items-end gap-1">
                    <Badge variant="secondary" className="rounded-xl">Impact: High</Badge>
                    <Badge variant="secondary" className="rounded-xl">Confidence: High</Badge>
                  </div>
                </div>
                <div className="mt-2 text-sm text-slate-700">
                  Phone cancel rate is running ~{fmtPct.format(trial2025Phone)} vs online ~{fmtPct.format(trial2025Online)} (2025 excl Dec). A <span className="font-medium">1pp</span> reduction in total trial cancels is roughly ~<span className="font-medium">{fmtInt.format(estExtraConversionsPerPp)}</span> incremental conversions.
                </div>
                <div className="mt-2 text-xs text-slate-600">
                  Do: script parity with online, agent QA scoring, “pause” option, and offer-framing A/B by call center / cohort.
                </div>
              </div>

              <div className="rounded-2xl border p-3">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <div className="font-semibold">2) Reverse-engineer May 2025</div>
                    <div className="mt-0.5 text-xs text-slate-600">Repeat what worked, stop guessing.</div>
                  </div>
                  <div className="flex flex-col items-end gap-1">
                    <Badge variant="secondary" className="rounded-xl">Impact: High</Badge>
                    <Badge variant="secondary" className="rounded-xl">Confidence: Medium</Badge>
                  </div>
                </div>
                <div className="mt-2 text-sm text-slate-700">
                  May 2025 is peak for GMV ({fmtMoney.format(k.peaks.gmv["2025"].Total)}) and claims ({fmtMoney.format(k.peaks.claims["2025"].Total)}). That’s either a killer playbook or a reporting artifact — either way, we need the story.
                </div>
                <div className="mt-2 text-xs text-slate-600">
                  Do: pull promo calendar + email drops + onsite changes; tie to joins, GMV/join, claims/join; run a “May-like” bundle in a low month.
                </div>
              </div>

              <div className="rounded-2xl border p-3">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <div className="font-semibold">3) De-risk placement concentration</div>
                    <div className="mt-0.5 text-xs text-slate-600">Single-point-of-failure vibes.</div>
                  </div>
                  <div className="flex flex-col items-end gap-1">
                    <Badge variant="secondary" className="rounded-xl">Impact: Medium</Badge>
                    <Badge variant="secondary" className="rounded-xl">Confidence: Medium</Badge>
                  </div>
                </div>
                <div className="mt-2 text-sm text-slate-700">
                  Inflow Experience is ~88%+ of mix in 2025. Great now — but if that placement underperforms, acquisition takes the hit.
                </div>
                <div className="mt-2 text-xs text-slate-600">
                  Do: incrementally scale Order Confirmation placements (top / bottom-right) with holdouts; measure incremental joins and GMV/join vs baseline.
                </div>
              </div>
            </div>
          </div>

          <div className="mt-4 text-xs text-slate-500">
            Data notes: Dec 2025 rows appear incomplete in multiple series. Several 0% billable-cancel months in late 2025 may reflect reporting logic rather than true zero churn.
          </div>
        </div>
      </div>
    </div>
  );
}
