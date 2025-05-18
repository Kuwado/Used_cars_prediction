"use client";

import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Avatar,
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  AppBar,
  Toolbar,
  Grid,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";
import { CarRental } from "@mui/icons-material";
import { useState } from "react";

const brands = [
  "Toyota",
  "Honda",
  "Hyundai",
  "Kia",
  "Mercedes",
  "BMW",
  "Ford",
  "Mitsubishi",
  "Suzuki",
  "VinFast",
  "Chevrolet",
  "MG",
  "Mazda",
  "Nissan",
  "Peugeot",
];

const hotCars = [
  { name: "Mazda 3 2018 1.5 Deluxe - Sedan" },
  { name: "Honda City 2021 RS 1.5 AT" },
  { name: "Toyota Innova 2018 2.0E MT" },
  { name: "Hyundai i10 2018 1.2 AT - hatchback" },
  { name: "Hyundai Accent 2020 1.4 AT" },
  { name: "Toyota Vios 2018 1.5E MT" },
];

const attributes = [
  { id: 1, label: "Hãng xe", placeholder: "Chọn hãng xe", key: "brand" },
  { id: 2, label: "Dòng xe", placeholder: "Nhập dòng xe", key: "model" },
  { id: 3, label: "Đời xe", placeholder: "Nhập đời xe", key: "year" },
  {
    id: 4,
    label: "Công tơ mét",
    placeholder: "Nhập số km đã đi",
    key: "mileage",
  },
  {
    id: 5,
    label: "Loại nhiên liệu",
    placeholder: "Nhập loại nhiên liệu",
    key: "fuel_type",
  },
  {
    id: 6,
    label: "Hộp số",
    placeholder: "Nhập loại hộp số",
    key: "transmission",
  },
  { id: 7, label: "Xuất xứ", placeholder: "Nhập xuất xứ", key: "origin" },
  { id: 8, label: "Loại xe", placeholder: "Nhập loại xe", key: "car_type" },
  {
    id: 9,
    label: "Số chỗ ngồi",
    placeholder: "Nhập số chỗ ngồi",
    key: "seats",
  },
];
type attributes = {
  id: number;
  label: string;
  placeholder: string;
  key: string;
};

export default function HomePage() {
  const [open, setOpen] = useState(false);
  const [selectedBrand, setSelectedBrand] = useState("");
  const [selectedAttribute, setSelectedAttribute] = useState(attributes[0]); // Mặc định chọn thuộc tính đầu tiên
  const [formData, setFormData] = useState<Record<string, string>>({}); // Lưu dữ liệu các trường

  const handleOpenDialog = (brand = "") => {
    setSelectedBrand(brand);
    setOpen(true);
  };

  const handleCloseDialog = () => {
    setOpen(false);
  };

  const handleAttributeClick = (attribute: attributes) => {
    setSelectedAttribute(attribute);
  };

  const handleInputChange = (e: any) => {
    setFormData({ ...formData, [selectedAttribute.label]: e.target.value });
  };

  return (
    <Box className="min-h-screen w-full bg-gray-50">
      <AppBar position="static" color="default" className="shadow-md">
        <Toolbar className="flex justify-between">
          <Typography variant="h6" className="font-bold">
            địnhgiaxe
          </Typography>
        </Toolbar>
      </AppBar>

      <Box className="flex justify-center items-center px-4 py-8">
        <Box className="flex flex-col md:flex-row gap-6 w-full max-w-6xl">
          <Box className="flex-1">
            <Card className="shadow-md rounded-xl h-full min-h-[500px] flex flex-col justify-between">
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Định giá ô tô cũ
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Chọn hãng xe để bắt đầu
                </Typography>

                <Box className="grid grid-cols-3 sm:grid-cols-6 gap-2 mt-2">
                  {brands.map((brand, idx) => (
                    <Button
                      key={idx}
                      variant="outlined"
                      startIcon={<CarRental />}
                      className="text-xs"
                      fullWidth
                      style={{ color: "black", borderColor: "black" }}
                      onClick={() => handleOpenDialog(brand)}
                    >
                      {brand}
                    </Button>
                  ))}
                </Box>

                <Box className="mt-6 text-center">
                  <Button
                    variant="contained"
                    size="large"
                    style={{ backgroundColor: "black", color: "white" }}
                    onClick={() => handleOpenDialog()}
                  >
                    Định giá ngay
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Box>

          <Box className="w-full md:w-[30%]">
            <Card className="shadow-md rounded-xl h-full min-h-[500px]">
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Được định giá nhiều nhất
                </Typography>
                <Box>
                  {hotCars.map((car, idx) => (
                    <Box key={idx} className="flex items-center gap-2 my-2">
                      <Avatar sx={{ width: 24, height: 24 }}>🚗</Avatar>
                      <Typography variant="body2">{car.name}</Typography>
                    </Box>
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Box>
        </Box>
      </Box>

      <Dialog open={open} onClose={handleCloseDialog} fullWidth maxWidth="md">
        <DialogTitle>Thông tin xe của bạn</DialogTitle>
        <DialogContent>
          <Grid container spacing={2}>
            {/* Danh sách thuộc tính */}
            <Grid item xs={4}>
              <List>
                {attributes.map((attribute) => (
                  <ListItem
                    key={attribute.id}
                    button
                    selected={selectedAttribute.id === attribute.id}
                    onClick={() => handleAttributeClick(attribute)}
                    style={{
                      backgroundColor:
                        selectedAttribute.id === attribute.id
                          ? "#f0f0f0"
                          : "white",
                    }}
                  >
                    <ListItemText primary={attribute.label} />
                  </ListItem>
                ))}
              </List>
            </Grid>

            {/* Trường nhập liệu */}
            <Grid item xs={8}>
              <Box>
                <Typography variant="h6" gutterBottom>
                  {selectedAttribute.label}
                </Typography>
                <TextField
                  placeholder={selectedAttribute.placeholder}
                  value={formData[selectedAttribute.key] || ""}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      [selectedAttribute.key]: e.target.value,
                    })
                  }
                  fullWidth
                />
                <Box mt={2}>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleCloseDialog}
                  >
                    Tiếp theo
                  </Button>
                </Box>
              </Box>
            </Grid>
          </Grid>
        </DialogContent>
      </Dialog>
    </Box>
  );
}
