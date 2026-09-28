---
name: nestjs-module-architect
description: Standardized procedure to generate modular NestJS domain modules, controllers, services, and DTOs with validation.
author: "NestJS Community, customized by innerpeace080"
version: "1.0.0"
license: "MIT"
metadata:
  origin_repo: "https://github.com/nestjs/nest"
  source_type: "community-curated"
  lineage: "forked-and-customized"
  last_upstream_sync: "2026-09-26T23:30:00Z"
---

# NestJS Module Architecture Runbook

## When to Use
Use this skill when adding a new domain feature, API resource, or module to a NestJS backend project.

---

## 1. Directory Structure of a Domain Module
```
src/users/
├── dto/
│   ├── create-user.dto.ts
│   └── update-user.dto.ts
├── entities/
│   └── user.entity.ts
├── users.controller.ts
├── users.service.ts
├── users.service.spec.ts
└── users.module.ts
```

---

## 2. Standard DTO Implementation
```typescript
import { IsEmail, IsNotEmpty, IsString, MinLength } from 'class-validator';

export class CreateUserDto {
  @IsEmail({}, { message: 'Invalid email address' })
  @IsNotEmpty()
  email: string;

  @IsString()
  @MinLength(2, { message: 'Name must be at least 2 characters long' })
  name: string;
}
```

---

## 3. Controller Implementation
```typescript
import { Controller, Post, Body, Get, Param, NotFoundException } from '@nestjs/common';
import { UsersService } from './users.service';
import { CreateUserDto } from './dto/create-user.dto';

@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Post()
  async create(@Body() createUserDto: CreateUserDto) {
    return this.usersService.create(createUserDto);
  }

  @Get(':id')
  async findOne(@Param('id') id: string) {
    const user = await this.usersService.findOne(id);
    if (!user) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }
    return user;
  }
}
```

