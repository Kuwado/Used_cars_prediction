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

export default function HomePage() {
  const [open, setOpen] = useState(false);
  const [selectedBrand, setSelectedBrand] = useState("");

  const handleOpenDialog = (brand = "") => {
    setSelectedBrand(brand);
    setOpen(true);
  };

  const handleCloseDialog = () => {
    setOpen(false);
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

      <Dialog open={open} onClose={handleCloseDialog} fullWidth maxWidth="sm">
        <DialogTitle>Thông tin xe của bạn</DialogTitle>
        <DialogContent>
          <Box className="flex flex-col gap-4">
            <TextField
              label="Hãng xe"
              value={selectedBrand}
              onChange={(e) => setSelectedBrand(e.target.value)}
              fullWidth
            />
            <TextField label="Dòng xe" fullWidth />
            <TextField label="Đời xe" fullWidth />
            <TextField label="Phiên bản" fullWidth />
            <TextField label="Màu xe" fullWidth />
            <TextField label="Công tơ mét" fullWidth />
            <TextField label="Nhu cầu định giá" fullWidth />
            <Button
              variant="contained"
              color="primary"
              onClick={handleCloseDialog}
            >
              Tiếp theo
            </Button>
          </Box>
        </DialogContent>
      </Dialog>
    </Box>
  );
}
