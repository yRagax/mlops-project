resource "aws_vpc" "chpp_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "CHPP VPC"
  }
}

resource "aws_subnet" "chpp_subnet_a" {
  vpc_id            = aws_vpc.chpp_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "${var.aws_region}a"

  tags = {
    Name = "CHPP Subnet A"
  }
}

resource "aws_subnet" "chpp_subnet_b" {
  vpc_id            = aws_vpc.chpp_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "${var.aws_region}b"

  tags = {
    Name = "CHPP Subnet B"
  }
}

resource "aws_subnet" "chpp_subnet_c" {
  vpc_id            = aws_vpc.chpp_vpc.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "${var.aws_region}c"

  tags = {
    Name = "CHPP Subnet C"
  }
}

resource "aws_internet_gateway" "chpp_igw" {
  vpc_id = aws_vpc.chpp_vpc.id

  tags = {
    Name = "CHPP IGW"
  }
}

resource "aws_route_table" "chpp_public_rt" {
  vpc_id = aws_vpc.chpp_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.chpp_igw.id
  }

  tags = {
    Name = "CHPP Public Route Table"
  }
}

resource "aws_route_table_association" "chpp_assoc_a" {
  subnet_id      = aws_subnet.chpp_subnet_a.id
  route_table_id = aws_route_table.chpp_public_rt.id
}

resource "aws_route_table_association" "chpp_assoc_b" {
  subnet_id      = aws_subnet.chpp_subnet_b.id
  route_table_id = aws_route_table.chpp_public_rt.id
}

resource "aws_route_table_association" "chpp_assoc_c" {
  subnet_id      = aws_subnet.chpp_subnet_c.id
  route_table_id = aws_route_table.chpp_public_rt.id
}
